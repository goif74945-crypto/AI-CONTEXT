import { beforeEach, describe, expect, it, vi } from "vitest";

// Integration with the real exported dispatch.ts functions. Only the external
// Prisma and Redis/BullMQ boundaries are mocked. NOT PostgreSQL/Redis proof.
type Row = {
  id: string; pipelineRunId: string; directiveId: string; idempotencyKey: string;
  status: string; attempts: number; lastError: string | null;
  updatedTick: bigint; enqueuedTick: bigint | null;
  directive: { input: string; mode: string; priority: string };
};
const mocks = vi.hoisted(() => ({
  state: { row: null as Row | null },
  enqueue: vi.fn(),
  findUnique: vi.fn(),
  findMany: vi.fn(),
  update: vi.fn(),
  updateMany: vi.fn(),
  emitAlarm: vi.fn(),
}));
vi.mock("../../packages/core/db.js", () => ({
  prisma: { directiveDispatch: {
    findUnique: mocks.findUnique,
    findMany: mocks.findMany,
    update: mocks.update,
    updateMany: mocks.updateMany,
  } },
}));
vi.mock("../../packages/queue/jobs.js", () => ({ enqueueDirective: mocks.enqueue }));
vi.mock("../../packages/core/tick.js", () => ({
  currentTick: () => 10n,
  currentTsaBatchTimeMs: () => 1_000_000n,
}));
vi.mock("../../packages/core/ulid.js", () => ({ generateUlid: () => "01FIXTUREID" }));
vi.mock("../../packages/obs/alarms.js", () => ({
  ALARM_NAME: { QUEUE_BACKLOG: "QUEUE_BACKLOG" }, emitAlarm: mocks.emitAlarm,
}));
import {
  cancelDirectiveDispatch, claimDirectiveDispatch, dispatchDirective,
} from "../../packages/queue/dispatch.js";

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason: Error) => void;
  const promise = new Promise<T>((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
function row(status = "PENDING", attempts = 0, lastError: string | null = null): Row {
  return {
    id: "d", pipelineRunId: "r", directiveId: "directive", idempotencyKey: "key",
    status, attempts, lastError, updatedTick: 1n, enqueuedTick: null,
    directive: { input: "work", mode: "strict", priority: "NORMAL" },
  };
}
function matches(w: Record<string, any>, current: Row): boolean {
  return Object.entries(w).every(([key, criterion]) => {
    if (key === "id" || key === "pipelineRunId") return current[key] === criterion;
    if (key === "status" && typeof criterion === "object") {
      return criterion.in?.includes(current.status) ?? false;
    }
    if (key === "attempts" && typeof criterion === "object") {
      return criterion.equals === current.attempts;
    }
    return current[key as keyof Row] === criterion;
  });
}
function write(data: Record<string, any>, current: Row) {
  for (const [key, value] of Object.entries(data)) {
    if (key === "attempts" && value && typeof value === "object") {
      current.attempts += value.increment ?? 0;
    } else {
      (current as any)[key] = value;
    }
  }
}
beforeEach(() => {
  vi.resetAllMocks();
  mocks.state.row = row();
  mocks.findUnique.mockImplementation(async ({ where }: any) => {
    const v = mocks.state.row;
    return v && matches(where, v) ? { ...v, directive: { ...v.directive } } : null;
  });
  mocks.findMany.mockResolvedValue([]);
  // Reproduce Prisma update({where:{id}}) exactly: stale ID update succeeds.
  mocks.update.mockImplementation(async ({ where, data }: any) => {
    const v = mocks.state.row;
    if (!v || !matches(where, v)) throw new Error("RecordNotFound");
    write(data, v); return { ...v };
  });
  // CAS semantics of Prisma updateMany: a status mismatch modifies no row.
  mocks.updateMany.mockImplementation(async ({ where, data }: any) => {
    const v = mocks.state.row;
    if (!v || !matches(where, v)) return { count: 0 };
    write(data, v); return { count: 1 };
  });
  mocks.enqueue.mockResolvedValue({ jobId: "key", idempotent: false });
});

describe("008 actual dispatch.ts cancellation boundaries (Prisma/BullMQ mocks)", () => {
  it("RED on original: CANCELLED must survive successful in-flight Redis enqueue", async () => {
    const entered = deferred<void>(), release = deferred<any>();
    mocks.enqueue.mockImplementation(async () => {
      entered.resolve(); return release.promise;
    });
    const sending = dispatchDirective("r");
    await entered.promise;
    await cancelDirectiveDispatch("r");
    release.resolve({ jobId: "key", idempotent: false });
    const result = await sending;
    expect(mocks.state.row?.status).toBe("CANCELLED");
    expect(mocks.state.row?.attempts).toBe(0);
    expect(mocks.state.row?.lastError).toBe("OWNER_CANCEL");
    expect(result).toMatchObject({ status: "CANCELLED", delivered: false });
  });
  it("RED on original: CANCELLED must survive in-flight Redis enqueue rejection", async () => {
    const entered = deferred<void>(), release = deferred<any>();
    mocks.enqueue.mockImplementation(async () => {
      entered.resolve(); return release.promise;
    });
    const sending = dispatchDirective("r");
    await entered.promise;
    await cancelDirectiveDispatch("r");
    release.reject(Object.assign(new Error("Redis offline"), { code: "QUEUE_UNAVAILABLE" }));
    const result = await sending;
    expect(mocks.state.row?.status).toBe("CANCELLED");
    expect(mocks.state.row?.attempts).toBe(0);
    expect(mocks.state.row?.lastError).toBe("OWNER_CANCEL");
    expect(result).toMatchObject({ status: "CANCELLED", delivered: false });
  });
  it("CANCELLED before dispatch never publishes to Redis", async () => {
    await cancelDirectiveDispatch("r");
    expect(await dispatchDirective("r")).toMatchObject({ status: "CANCELLED", delivered: false });
    expect(mocks.enqueue).not.toHaveBeenCalled();
  });
  it("ordinary enqueue transitions PENDING -> ENQUEUED exactly once", async () => {
    expect(await dispatchDirective("r")).toMatchObject({ status: "ENQUEUED", delivered: true });
    expect(mocks.state.row).toMatchObject({ status: "ENQUEUED", attempts: 1, lastError: null });
  });
  it("worker may claim PENDING while Redis publish is in-flight without producer overwriting PROCESSING", async () => {
    const entered = deferred<void>(), release = deferred<any>();
    mocks.enqueue.mockImplementation(async () => { entered.resolve(); return release.promise; });
    const sending = dispatchDirective("r");
    await entered.promise;
    expect(await claimDirectiveDispatch("r")).toBe("CLAIMED");
    release.resolve({ jobId: "key", idempotent: false });
    const result = await sending;
    expect(mocks.state.row?.status).toBe("PROCESSING");
    expect(result.status).toBe("PROCESSING");
    expect(await claimDirectiveDispatch("r")).toBe("BUSY");
  });
  it("Redis enqueue failure records FAILED only if PENDING is still current", async () => {
    mocks.enqueue.mockRejectedValue(Object.assign(new Error("offline"), { code: "QUEUE_UNAVAILABLE" }));
    expect(await dispatchDirective("r")).toMatchObject({
      status: "FAILED", delivered: false, errorCode: "QUEUE_UNAVAILABLE",
    });
    expect(mocks.state.row).toMatchObject({ status: "FAILED", attempts: 1, lastError: "QUEUE_UNAVAILABLE" });
  });
  it("DB CAS failure after Redis publish cannot be caught as enqueue failure", async () => {
    mocks.updateMany.mockRejectedValueOnce(new Error("DB_WRITE_UNAVAILABLE"));
    await expect(dispatchDirective("r")).rejects.toThrow("DB_WRITE_UNAVAILABLE");
    expect(mocks.state.row).toMatchObject({ status: "PENDING", attempts: 0 });
    expect(mocks.update).not.toHaveBeenCalled();
  });
  it("FAILED retries require allowlist, cap, and explicit authorization", async () => {
    mocks.state.row = row("FAILED", 1, "QUEUE_UNAVAILABLE");
    expect(await dispatchDirective("r")).toMatchObject({ status: "FAILED", delivered: false });
    expect(mocks.enqueue).not.toHaveBeenCalled();
    const policy = { enabled: true, maxAttempts: 3, safeErrorCodes: ["QUEUE_UNAVAILABLE"] };
    expect(await dispatchDirective("r", policy)).toMatchObject({ status: "ENQUEUED", delivered: true });
    expect(mocks.enqueue).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
      retryAuthorization: expect.anything(),
    }));
    mocks.state.row = row("FAILED", 3, "QUEUE_UNAVAILABLE");
    mocks.enqueue.mockClear();
    expect(await dispatchDirective("r", policy)).toMatchObject({ status: "FAILED", delivered: false });
    expect(mocks.enqueue).not.toHaveBeenCalled();
  });
  it("two active producers cannot both advance attempts for same version", async () => {
    const both = deferred<void>(), releases = [deferred<any>(), deferred<any>()];
    let entered = 0;
    mocks.enqueue.mockImplementation(async () => {
      const n = entered++;
      if (entered === 2) both.resolve();
      return releases[n]!.promise;
    });
    const first = dispatchDirective("r");
    const second = dispatchDirective("r");
    await both.promise;
    releases[0]!.resolve({ jobId: "key", idempotent: false });
    releases[1]!.resolve({ jobId: "key", idempotent: true });
    const results = await Promise.all([first, second]);
    expect(mocks.state.row).toMatchObject({ status: "ENQUEUED", attempts: 1 });
    expect(results.every(v => v.delivered)).toBe(true);
  });
});
