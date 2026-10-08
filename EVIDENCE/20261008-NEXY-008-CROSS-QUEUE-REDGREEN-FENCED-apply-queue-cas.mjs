import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

/** EXECUTION 008: guarded source patch candidate. Only run inside an isolated
 * checkout after fetching/inspecting current HEAD. Never force/rebase. */
const EXPECT_HEAD = "44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08";
const EXPECT_BLOB = "002eef253ce836e2cd0e200f5d15cb5042cdeb29";
const file = "packages/queue/dispatch.ts";
const git = (...a) => execFileSync("git", a, { encoding: "utf8" }).trim();
if (git("rev-parse", "--abbrev-ref", "HEAD") !== "NEXY.ai") {
  throw new Error("BRANCH_FENCE_VIOLATION");
}
if (git("rev-parse", "HEAD") !== EXPECT_HEAD) {
  throw new Error("HEAD_DRIFT_REVIEW_REQUIRED");
}
if (git("hash-object", file) !== EXPECT_BLOB) {
  throw new Error("SOURCE_BLOB_DRIFT_REVIEW_REQUIRED");
}
if (git("status", "--porcelain", "--", file)) {
  throw new Error("SOURCE_FILE_DIRTY_REVIEW_REQUIRED");
}
let code = readFileSync(file, "utf8").replace(/\r\n/g, "\n");
const scope = [
  "  if (row.status === DISPATCH_STATUS.CANCELLED) {",
  "    return { status: DISPATCH_STATUS.CANCELLED, delivered: false, idempotent: true };",
  "  }",
].join("\n");
if (code.split(scope).length !== 2) throw new Error("CANCELLED_GUARD_ANCHOR_CHANGED");
code = code.replace(scope, scope + [
  "",
  "  if (row.status === DISPATCH_STATUS.PROCESSING) {",
  "    return { status: DISPATCH_STATUS.PROCESSING, delivered: true, idempotent: true };",
  "  }",
].join("\n"));
const anchor = "/**\n * Enqueue one durable dispatch row and advance its delivery state.";
if (code.split(anchor).length !== 2) throw new Error("READBACK_HELPER_ANCHOR_CHANGED");
const helper = `/**
 * Report the durable truth after an optimistic producer CAS loses.
 * Redis publication may have succeeded: do not rewrite a later terminal state.
 */
async function readCurrentDispatchOutcome(rowId: string): Promise<DispatchAttemptResult> {
  const fresh = await prisma.directiveDispatch.findUnique({
    where: { id: rowId },
    select: { status: true, lastError: true },
  });
  if (!fresh) return { status: "MISSING", delivered: false, idempotent: false };
  switch (fresh.status) {
    case DISPATCH_STATUS.COMPLETED:
    case DISPATCH_STATUS.PROCESSING:
    case DISPATCH_STATUS.ENQUEUED:
      return { status: fresh.status, delivered: true, idempotent: true };
    case DISPATCH_STATUS.CANCELLED:
      return { status: DISPATCH_STATUS.CANCELLED, delivered: false, idempotent: true };
    case DISPATCH_STATUS.FAILED:
      return {
        status: DISPATCH_STATUS.FAILED, delivered: false, idempotent: true,
        errorCode: fresh.lastError ?? "QUEUE_UNAVAILABLE",
      };
    case DISPATCH_STATUS.PENDING:
      return { status: DISPATCH_STATUS.PENDING, delivered: false, idempotent: true };
    default:
      throw new Error("QUEUE_DISPATCH_STATE_INVALID");
  }
}

`;
code = code.replace(anchor, helper + anchor);
const start = "  try {\n    const enqueuedAtMs = requireQueueAuthorityTimeMs();";
const end = "\n}\n\n/**\n * Reconcile every durable row";
const i = code.indexOf(start);
const j = code.indexOf(end, i);
if (i < 0 || j < 0 || code.indexOf(start, i + 1) !== -1) {
  throw new Error("DISPATCH_TRANSITION_ANCHOR_CHANGED");
}
const candidate = `  let enqueuedAtMs: bigint;
  let enqueueResult: Awaited<ReturnType<typeof enqueueDirective>>;
  try {
    enqueuedAtMs = requireQueueAuthorityTimeMs();
    enqueueResult = await enqueueDirective(jobData(row), {
      idempotencyKey: row.idempotencyKey,
      enqueuedAtMs,
      ...(row.status === DISPATCH_STATUS.FAILED
        ? {
            retryAuthorization: {
              row: {
                status: row.status,
                attempts: row.attempts,
                lastError: row.lastError,
              },
              policy: retryPolicy,
            },
          }
        : {}),
    });
  } catch (error) {
    // The catch encloses ONLY queue/time production, never a DB CAS or read.
    const errorCode = dispatchErrorCode(error);
    const failed = await prisma.directiveDispatch.updateMany({
      where: { id: row.id, status: row.status, attempts: row.attempts },
      data: {
        status: DISPATCH_STATUS.FAILED,
        attempts: { increment: 1 },
        updatedTick: currentTick(),
        lastError: errorCode,
      },
    });
    if (failed.count !== 1) return readCurrentDispatchOutcome(row.id);
    return { status: DISPATCH_STATUS.FAILED, delivered: false, idempotent: false, errorCode };
  }

  // Conditional DB transition: a cancellation/claim/completion beats this
  // producer acknowledgement, even if the Redis job is already published.
  const saved = await prisma.directiveDispatch.updateMany({
    where: { id: row.id, status: row.status, attempts: row.attempts },
    data: {
      status: DISPATCH_STATUS.ENQUEUED,
      attempts: { increment: 1 },
      updatedTick: currentTick(),
      enqueuedTick: enqueuedAtMs,
      lastError: null,
    },
  });
  if (saved.count !== 1) return readCurrentDispatchOutcome(row.id);
  return {
    status: DISPATCH_STATUS.ENQUEUED,
    delivered: true,
    idempotent: enqueueResult.idempotent,
  };`;
code = code.slice(0, i) + candidate + code.slice(j);
writeFileSync(file, code, "utf8");
console.log("PATCH_APPLIED_TO_ISOLATED_CHECKOUT=1");
console.log("ORIGINAL_HEAD=" + EXPECT_HEAD);
console.log("ORIGINAL_BLOB=" + EXPECT_BLOB);
