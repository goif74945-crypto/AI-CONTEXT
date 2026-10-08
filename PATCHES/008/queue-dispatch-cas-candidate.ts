// Durable DB -> BullMQ dispatch.
// A directive is accepted in the database before it is considered delivered.
// PENDING/ENQUEUED rows are reconciled after restarts. FAILED rows are never
// replayed implicitly: an explicit safe-error allowlist and attempt cap are
// required before a retry can be selected.

import { Prisma } from "@prisma/client";
import { currentTick, currentTsaBatchTimeMs } from "../core/tick.js";
import { generateUlid } from "../core/ulid.js";
import { prisma } from "../core/db.js";
import { enqueueDirective, type DirectiveJobData } from "./jobs.js";
import { ALARM_NAME, emitAlarm } from "../obs/alarms.js";
import {
  FAILED_RETRY_DISABLED,
  isFailedDispatchRetryAllowed,
  isFailedDispatchRetryPolicy,
  type FailedDispatchRetryPolicy,
} from "./retry-policy.js";

export const DISPATCH_STATUS = {
  PENDING: "PENDING",
  ENQUEUED: "ENQUEUED",
  PROCESSING: "PROCESSING",
  COMPLETED: "COMPLETED",
  FAILED: "FAILED",
  CANCELLED: "CANCELLED",
} as const;

export type DispatchStatus = (typeof DISPATCH_STATUS)[keyof typeof DISPATCH_STATUS];

export interface NewDispatchRecord {
  directiveId: string;
  pipelineRunId: string;
  idempotencyKey: string;
  createdTick: bigint;
}

export async function createDirectiveDispatch(
  tx: Prisma.TransactionClient,
  record: NewDispatchRecord,
): Promise<void> {
  await tx.directiveDispatch.create({
    data: {
      id: generateUlid(),
      directiveId: record.directiveId,
      pipelineRunId: record.pipelineRunId,
      idempotencyKey: record.idempotencyKey,
      status: DISPATCH_STATUS.PENDING,
      attempts: 0,
      createdTick: record.createdTick,
      updatedTick: record.createdTick,
    },
  });
}

function jobData(row: {
  directiveId: string;
  pipelineRunId: string;
  idempotencyKey: string;
  directive: {
    input: string;
    mode: string;
    priority: string;
  };
}): DirectiveJobData {
  return {
    directiveId: row.directiveId,
    pipelineRunId: row.pipelineRunId,
    input: row.directive.input,
    mode: row.directive.mode,
    priority: row.directive.priority,
    idempotencyKey: row.idempotencyKey,
  };
}

function dispatchErrorCode(error: unknown): string {
  if (error && typeof error === "object" && "code" in error) {
    const code = (error as { code?: unknown }).code;
    if (typeof code === "string" && /^[A-Z0-9_]+$/.test(code)) return code;
  }
  return "QUEUE_UNAVAILABLE";
}

function requireQueueAuthorityTimeMs(): bigint {
  try {
    return currentTsaBatchTimeMs();
  } catch {
    const error = new Error("TSA_TIME_AUTHORITY_UNAVAILABLE");
    (error as NodeJS.ErrnoException).code = "TSA_TIME_AUTHORITY_UNAVAILABLE";
    throw error;
  }
}

export interface DispatchAttemptResult {
  status: DispatchStatus | "MISSING";
  delivered: boolean;
  idempotent: boolean;
  errorCode?: string;
}

/**
 * Enqueue one durable dispatch row and advance its delivery state. This is
 * safe to call repeatedly, including when Redis was unavailable after the DB
 * transaction committed.
 */
export async function dispatchDirective(
  pipelineRunId: string,
  retryPolicy: FailedDispatchRetryPolicy = FAILED_RETRY_DISABLED,
): Promise<DispatchAttemptResult> {
  const row = await prisma.directiveDispatch.findUnique({
    where: { pipelineRunId },
    include: { directive: true },
  });
  if (!row) return { status: "MISSING", delivered: false, idempotent: false };
  if (row.status === DISPATCH_STATUS.COMPLETED) {
    return { status: DISPATCH_STATUS.COMPLETED, delivered: true, idempotent: true };
  }
  if (row.status === DISPATCH_STATUS.CANCELLED) {
    return { status: DISPATCH_STATUS.CANCELLED, delivered: false, idempotent: true };
  }
  if (row.status === DISPATCH_STATUS.PROCESSING) {
    return { status: DISPATCH_STATUS.PROCESSING, delivered: true, idempotent: true };
  }
  if (
    row.status === DISPATCH_STATUS.FAILED
    && !isFailedDispatchRetryAllowed(
      { status: row.status, attempts: row.attempts, lastError: row.lastError },
      retryPolicy,
    )
  ) {
    return {
      status: DISPATCH_STATUS.FAILED,
      delivered: false,
      idempotent: true,
      errorCode: row.lastError ?? "QUEUE_FAILED_RETRY_DISABLED",
    };
  }
  if (
    row.status !== DISPATCH_STATUS.PENDING
    && row.status !== DISPATCH_STATUS.ENQUEUED
    && row.status !== DISPATCH_STATUS.FAILED
  ) {
    throw new Error("QUEUE_DISPATCH_STATUS_INVALID");
  }

  // An external Redis enqueue is not atomic with the database transition.
  // Re-read durable state after any losing CAS; terminal states are immutable.
  const resultAfterConflict = async (): Promise<DispatchAttemptResult> => {
    const current = await prisma.directiveDispatch.findUnique({
      where: { id: row.id },
      select: { status: true, lastError: true },
    });
    if (!current) return { status: "MISSING", delivered: false, idempotent: false };
    switch (current.status) {
      case DISPATCH_STATUS.CANCELLED:
        return { status: DISPATCH_STATUS.CANCELLED, delivered: false, idempotent: true };
      case DISPATCH_STATUS.COMPLETED:
      case DISPATCH_STATUS.PROCESSING:
      case DISPATCH_STATUS.ENQUEUED:
        return { status: current.status, delivered: true, idempotent: true };
      case DISPATCH_STATUS.FAILED:
        return {
          status: DISPATCH_STATUS.FAILED,
          delivered: false,
          idempotent: true,
          errorCode: current.lastError ?? "QUEUE_FAILED_RETRY_DISABLED",
        };
      case DISPATCH_STATUS.PENDING:
        return {
          status: DISPATCH_STATUS.PENDING,
          delivered: false,
          idempotent: true,
          errorCode: "QUEUE_DISPATCH_STATE_CONFLICT",
        };
      default:
        throw new Error("QUEUE_DISPATCH_STATUS_INVALID");
    }
  };

  const expected = {
    id: row.id,
    status: row.status,
    attempts: row.attempts,
    lastError: row.lastError,
  };
  let enqueuedAtMs: bigint;
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
    // Only time-authority/enqueue errors are delivery failures. A database
    // CAS exception must propagate, never be converted into a second write.
    const errorCode = dispatchErrorCode(error);
    const changed = await prisma.directiveDispatch.updateMany({
      where: expected,
      data: {
        status: DISPATCH_STATUS.FAILED,
        attempts: { increment: 1 },
        updatedTick: currentTick(),
        lastError: errorCode,
      },
    });
    if (changed.count !== 1) return resultAfterConflict();
    return { status: DISPATCH_STATUS.FAILED, delivered: false, idempotent: false, errorCode };
  }

  const changed = await prisma.directiveDispatch.updateMany({
    where: expected,
    data: {
      status: DISPATCH_STATUS.ENQUEUED,
      attempts: { increment: 1 },
      updatedTick: currentTick(),
      enqueuedTick: enqueuedAtMs,
      lastError: null,
    },
  });
  if (changed.count !== 1) return resultAfterConflict();
  return {
    status: DISPATCH_STATUS.ENQUEUED,
    delivered: true,
    idempotent: enqueueResult.idempotent,
  };
}
/**
 * Reconcile every durable row that has not reached the worker. ENQUEUED rows
 * are included because Redis may have lost the job after the DB update.
 */
export async function reconcilePendingDispatches(
  limit = 50,
  retryPolicy: FailedDispatchRetryPolicy = FAILED_RETRY_DISABLED,
): Promise<{
  attempted: number;
  delivered: number;
  failed: number;
}> {
  // A malformed caller policy cannot widen the retry surface. Treat it as
  // the canonical disabled policy before constructing the database selector.
  const effectiveRetryPolicy = isFailedDispatchRetryPolicy(retryPolicy)
    ? retryPolicy
    : FAILED_RETRY_DISABLED;
  const retryFailedWhere = effectiveRetryPolicy.enabled
    && effectiveRetryPolicy.maxAttempts > 0
    && effectiveRetryPolicy.safeErrorCodes.length > 0
    ? [{
        status: DISPATCH_STATUS.FAILED,
        attempts: { lt: effectiveRetryPolicy.maxAttempts },
        lastError: { in: [...effectiveRetryPolicy.safeErrorCodes] },
      }]
    : [];

  const rows = await prisma.directiveDispatch.findMany({
    where: {
      OR: [
        { status: { in: [DISPATCH_STATUS.PENDING, DISPATCH_STATUS.ENQUEUED] } },
        ...retryFailedWhere,
      ],
    },
    orderBy: { updatedTick: "asc" },
    take: limit,
    select: { pipelineRunId: true },
  });

  if (rows.length > 0) {
    void emitAlarm(ALARM_NAME.QUEUE_BACKLOG, {
      severity: "WARN",
      source: "queue-reconciler",
      dedupeKey: "pending-dispatch",
      payload: { pending_count: rows.length },
    });
  }

  let delivered = 0;
  let failed = 0;
  for (const row of rows) {
    const result = await dispatchDirective(row.pipelineRunId, effectiveRetryPolicy);
    if (result.delivered) delivered++;
    else failed++;
  }
  return { attempted: rows.length, delivered, failed };
}

export function startDispatchReconciler(
  intervalMs = 5_000,
  retryPolicy: FailedDispatchRetryPolicy = FAILED_RETRY_DISABLED,
): () => void {
  let running = false;
  const timer = setInterval(() => {
    if (running) return;
    running = true;
    void reconcilePendingDispatches(50, retryPolicy)
      .then((result) => {
        if (result.failed > 0) {
          process.stderr.write(`[QUEUE_RECONCILE] failed=${result.failed} delivered=${result.delivered}\n`);
        }
      })
      .catch(() => process.stderr.write("[QUEUE_RECONCILE] dependency failure\n"))
      .finally(() => { running = false; });
  }, intervalMs);
  timer.unref();
  return () => clearInterval(timer);
}

export async function claimDirectiveDispatch(
  pipelineRunId: string,
): Promise<"CLAIMED" | "COMPLETED" | "CANCELLED" | "BUSY" | "MISSING"> {
  const row = await prisma.directiveDispatch.findUnique({
    where: { pipelineRunId },
    select: { id: true, status: true },
  });
  if (!row) return "MISSING";
  if (row.status === DISPATCH_STATUS.COMPLETED) return "COMPLETED";
  if (row.status === DISPATCH_STATUS.CANCELLED) return "CANCELLED";
  if (row.status === DISPATCH_STATUS.PROCESSING) return "BUSY";

  const claimed = await prisma.directiveDispatch.updateMany({
    where: {
      id: row.id,
      status: { in: [DISPATCH_STATUS.PENDING, DISPATCH_STATUS.ENQUEUED] },
    },
    data: { status: DISPATCH_STATUS.PROCESSING, updatedTick: currentTick() },
  });
  return claimed.count === 1 ? "CLAIMED" : "BUSY";
}

export async function completeDirectiveDispatch(pipelineRunId: string): Promise<void> {
  await prisma.directiveDispatch.updateMany({
    where: { pipelineRunId, status: DISPATCH_STATUS.PROCESSING },
    data: { status: DISPATCH_STATUS.COMPLETED, updatedTick: currentTick() },
  });
}

export async function failDirectiveDispatch(pipelineRunId: string, errorCode: string): Promise<void> {
  await prisma.directiveDispatch.updateMany({
    where: { pipelineRunId, status: { in: [DISPATCH_STATUS.PROCESSING, DISPATCH_STATUS.ENQUEUED] } },
    data: { status: DISPATCH_STATUS.FAILED, updatedTick: currentTick(), lastError: errorCode },
  });
}

export async function cancelDirectiveDispatch(pipelineRunId: string): Promise<void> {
  await prisma.directiveDispatch.updateMany({
    where: {
      pipelineRunId,
      status: {
        in: [
          DISPATCH_STATUS.PENDING,
          DISPATCH_STATUS.ENQUEUED,
          DISPATCH_STATUS.PROCESSING,
          DISPATCH_STATUS.FAILED,
        ],
      },
    },
    data: {
      status: DISPATCH_STATUS.CANCELLED,
      updatedTick: currentTick(),
      lastError: "OWNER_CANCEL",
    },
  });
}
