// Integration with the REAL packages/queue/dispatch.ts exports; Prisma and BullMQ boundary mocked.
// Apply under tests/integration/queue-cancel-race-008.spec.ts on the SOURCE-LOCKED product HEAD.
// Execution-008 status: NOT_RUN, requires npm ci + npx vitest.
import { beforeEach, describe, expect, it, vi } from "vitest";

const fixture = vi.hoisted(() => ({
  row: {
    id: "dispatch-1", pipelineRunId: "run-1", directiveId: "directive-1",
    idempotencyKey: "idem-1", status: "PENDING", attempts: 0,
    lastError: null as string | null, createdTick: 1n, updatedTick: 1n,
    enqueuedTick: null as bigint | null,
    directive: { input: "payload", mode: "RUN", priority: "NORMAL" },
  },
  enqueue: vi.fn<(...args: unknown[]) => Promise<{ jobId: string; idempotent: boolean }>>(),
  published: false,
  failCas: false,
}));

vi.mock("../../packages/core/db.js", () => {
  const current = fixture.row;
  function matches(where: Record<string, unknown>): boolean {
    for (const [key, value] of Object.entries(where)) {
      const present = (current as unknown as Record<string, unknown>)[key];
      if (key === "status" && typeof value === "object" && value !== null && "in" in value) {
        if (!(value.in as string[]).includes(current.status)) return false;
      } else if (value !== present) return false;
    }
    return true;
  }
  function write(data: Record<string, unknown>): void {
    if (typeof data.status === "string") current.status = data.status;
    if (typeof data.lastError === "string" || data.lastError === null) current.lastError = data.lastError as string | null;
    if (typeof data.updatedTick === "bigint") current.updatedTick = data.updatedTick;
    if (typeof data.enqueuedTick === "bigint") current.enqueuedTick = data.enqueuedTick;
    if (typeof data.attempts === "object" && data.attempts !== null && "increment" in data.attempts) {
      current.attempts += Number(data.attempts.increment);
    }
  }
  return {
    prisma: {
      directiveDispatch: {
        findUnique: async (args: {where: Record<string, unknown>}) =>
          matches(args.where) ? { ...current, directive: { ...current.directive } } : null,
        update: async (args: {where: Record<string, unknown>; data: Record<string, unknown>}) => {
          if (!matches(args.where)) throw new Error("ROW_NOT_FOUND");
          write(args.data); return { ...current };
        },
        updateMany: async (args: {where: Record<string, unknown>; data: Record<string, unknown>}) => {
          if (fixture.failCas) throw new Error("MOCK_DB_UNAVAILABLE");
          if (!matches(args.where)) return { count: 0 };
          write(args.data); return { count: 1 };
        },
        findMany: async () => [],
      },
    },
  };
});
vi.mock("../../packages/core/tick.js", () => ({
  currentTick: () => 12345n,
  currentTsaBatchTimeMs: () => 900000n, // isolated MOCK boundary only; not production TSA
}));
vi.mock("../../packages/core/ulid.js", () => ({ generateUlid: () => "test-ulid" }));
vi.mock("../../packages/queue/jobs.js", () => ({ enqueueDirective: fixture.enqueue }));
vi.mock("../../packages/obs/alarms.js", () => ({
  ALARM_NAME: { QUEUE_BACKLOG: "QUEUE_BACKLOG" },
  emitAlarm: vi.fn(async () => undefined),
}));

import {
  dispatchDirective, cancelDirectiveDispatch, claimDirectiveDispatch,
  completeDirectiveDispatch,
} from "../../packages/queue/dispatch.js";

function deferred(): { wait: Promise<void>; release: () => void } {
  let release!: () => void;
  const wait = new Promise<void>((resolve) => { release = resolve; });
  return { wait, release };
}
function installDelayedEnqueue(throwCode?: string, markPublished = true) {
  const entered = deferred();
  const continuation = deferred();
  fixture.enqueue.mockImplementation(async () => {
    if (markPublished) fixture.published = true;
    entered.release();
    await continuation.wait;
    if (throwCode) throw Object.assign(new Error(throwCode), { code: throwCode });
    return { jobId: "idem-1", idempotent: false };
  });
  return { entered: entered.wait, continue: continuation.release };
}
beforeEach(() => {
  Object.assign(fixture.row, {
    status: "PENDING", attempts: 0, lastError: null, updatedTick: 1n, enqueuedTick: null,
  });
  fixture.published = false;
  fixture.failCas = false;
  fixture.enqueue.mockReset();
  fixture.enqueue.mockResolvedValue({ jobId: "idem-1", idempotent: false });
});

describe("Queue cancellation vs actual dispatch.ts functions (MOCK_INTEGRATION)", () => {
  it("RED on old source: concurrent cancel while Redis publishing never resurrects CANCELLED", async () => {
    const gate = installDelayedEnqueue(undefined, true);
    const publishing = dispatchDirective("run-1");
    await gate.entered;
    await cancelDirectiveDispatch("run-1");
    gate.continue();
    const result = await publishing;
    expect(fixture.published).toBe(true);
    expect(fixture.row.status).toBe("CANCELLED");
    expect(fixture.row.lastError).toBe("OWNER_CANCEL");
    expect(fixture.row.attempts).toBe(0);
    expect(result).toMatchObject({ status: "CANCELLED", delivered: false });
    expect(await claimDirectiveDispatch("run-1")).toBe("CANCELLED");
  });
  it("RED on old source: enqueue error after cancellation cannot write FAILED", async () => {
    const gate = installDelayedEnqueue("QUEUE_UNAVAILABLE", false);
    const publishing = dispatchDirective("run-1");
    await gate.entered;
    await cancelDirectiveDispatch("run-1");
    gate.continue();
    const result = await publishing;
    expect(fixture.row).toMatchObject({ status: "CANCELLED", attempts: 0, lastError: "OWNER_CANCEL" });
    expect(result).toMatchObject({ status: "CANCELLED", delivered: false });
  });
  it("cancel BEFORE producer is a no-enqueue idempotent exit", async () => {
    await cancelDirectiveDispatch("run-1");
    const result = await dispatchDirective("run-1");
    expect(result.status).toBe("CANCELLED");
    expect(fixture.enqueue).not.toHaveBeenCalled();
  });
  it("successful enqueue advances exactly once", async () => {
    const result = await dispatchDirective("run-1");
    expect(result).toMatchObject({ status: "ENQUEUED", delivered: true });
    expect(fixture.row).toMatchObject({ status: "ENQUEUED", attempts: 1, lastError: null });
    expect(fixture.row.enqueuedTick).toBe(900000n);
  });
  it("worker claims PENDING before producer CAS, stale producer must NOT unclaim PROCESSING", async () => {
    const gate = installDelayedEnqueue();
    const publishing = dispatchDirective("run-1");
    await gate.entered;
    expect(await claimDirectiveDispatch("run-1")).toBe("CLAIMED");
    gate.continue();
    const result = await publishing;
    expect(fixture.row.status).toBe("PROCESSING");
    expect(result).toMatchObject({ status: "PROCESSING", delivered: true });
  });
  it("worker completes before producer CAS, stale producer must NOT resurrect COMPLETED", async () => {
    const gate = installDelayedEnqueue();
    const publishing = dispatchDirective("run-1");
    await gate.entered;
    expect(await claimDirectiveDispatch("run-1")).toBe("CLAIMED");
    await completeDirectiveDispatch("run-1");
    gate.continue();
    const result = await publishing;
    expect(fixture.row.status).toBe("COMPLETED");
    expect(result).toMatchObject({ status: "COMPLETED", delivered: true });
  });
  it("enqueue failure sets FAILED with one attempt if no intervening writer", async () => {
    fixture.enqueue.mockRejectedValue(Object.assign(new Error("Redis"), { code: "QUEUE_UNAVAILABLE" }));
    const result = await dispatchDirective("run-1");
    expect(result).toMatchObject({ status: "FAILED", delivered: false, errorCode: "QUEUE_UNAVAILABLE" });
    expect(fixture.row.attempts).toBe(1);
  });
  it("default FAILED retry is prohibited and does not enqueue", async () => {
    Object.assign(fixture.row, { status: "FAILED", attempts: 1, lastError: "QUEUE_UNAVAILABLE" });
    const result = await dispatchDirective("run-1");
    expect(result.delivered).toBe(false);
    expect(fixture.enqueue).not.toHaveBeenCalled();
  });
  it("allowed FAILED retry is honored without exceeding max attempts", async () => {
    const policy = { enabled: true, maxAttempts: 2, safeErrorCodes: ["QUEUE_UNAVAILABLE"] };
    Object.assign(fixture.row, { status: "FAILED", attempts: 1, lastError: "QUEUE_UNAVAILABLE" });
    const result = await dispatchDirective("run-1", policy);
    expect(result.delivered).toBe(true);
    expect(fixture.row.attempts).toBe(2);
    Object.assign(fixture.row, { status: "FAILED", attempts: 2, lastError: "QUEUE_UNAVAILABLE" });
    fixture.enqueue.mockClear();
    const denied = await dispatchDirective("run-1", policy);
    expect(denied.delivered).toBe(false);
    expect(fixture.enqueue).not.toHaveBeenCalled();
  });
  it("DB CAS exception propagates instead of being mislabeled as a Redis failure", async () => {
    fixture.failCas = true;
    await expect(dispatchDirective("run-1")).rejects.toThrow("MOCK_DB_UNAVAILABLE");
    expect(fixture.row.status).toBe("PENDING");
  });
});
