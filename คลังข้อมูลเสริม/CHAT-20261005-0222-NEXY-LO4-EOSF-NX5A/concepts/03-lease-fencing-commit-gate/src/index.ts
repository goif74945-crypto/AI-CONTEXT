import { ContractError, assertNonEmpty, assertSafeInt } from "../../../src/canonical.js";

export interface LeaseState {
  readonly resourceId: string;
  readonly holderId: string;
  readonly fence: number;
  readonly validThroughSeq: number;
  readonly revoked: boolean;
}

export interface CommitAttempt {
  readonly resourceId: string;
  readonly workerId: string;
  readonly observedFence: number;
  readonly atSeq: number;
}

export type FenceDecision =
  | { readonly verdict: "ALLOW"; readonly fence: number }
  | { readonly verdict: "FREEZE"; readonly reason: "WRONG_RESOURCE" | "REVOKED" | "WRONG_HOLDER" | "STALE_FENCE" | "FUTURE_FENCE" | "LEASE_EXPIRED" };

export function validateLease(lease: LeaseState): void {
  assertNonEmpty(lease.resourceId, "resourceId");
  assertNonEmpty(lease.holderId, "holderId");
  assertSafeInt(lease.fence, "fence", 1);
  assertSafeInt(lease.validThroughSeq, "validThroughSeq", 0);
}

export function acquireNextLease(previous: LeaseState | null, resourceId: string, holderId: string, validThroughSeq: number): LeaseState {
  assertNonEmpty(resourceId, "resourceId"); assertNonEmpty(holderId, "holderId"); assertSafeInt(validThroughSeq, "validThroughSeq", 0);
  if (previous) {
    validateLease(previous);
    if (previous.resourceId !== resourceId) throw new ContractError("cannot advance a fence for a different resource");
  }
  const fence = previous ? previous.fence + 1 : 1;
  if (!Number.isSafeInteger(fence)) throw new ContractError("fence overflow");
  return { resourceId, holderId, fence, validThroughSeq, revoked: false };
}

export function authorizeCommit(lease: LeaseState, attempt: CommitAttempt): FenceDecision {
  validateLease(lease);
  assertNonEmpty(attempt.resourceId, "attempt.resourceId"); assertNonEmpty(attempt.workerId, "attempt.workerId");
  assertSafeInt(attempt.observedFence, "observedFence", 1); assertSafeInt(attempt.atSeq, "atSeq", 0);
  if (attempt.resourceId !== lease.resourceId) return { verdict: "FREEZE", reason: "WRONG_RESOURCE" };
  if (lease.revoked) return { verdict: "FREEZE", reason: "REVOKED" };
  if (attempt.workerId !== lease.holderId) return { verdict: "FREEZE", reason: "WRONG_HOLDER" };
  if (attempt.observedFence < lease.fence) return { verdict: "FREEZE", reason: "STALE_FENCE" };
  if (attempt.observedFence > lease.fence) return { verdict: "FREEZE", reason: "FUTURE_FENCE" };
  if (attempt.atSeq > lease.validThroughSeq) return { verdict: "FREEZE", reason: "LEASE_EXPIRED" };
  return { verdict: "ALLOW", fence: lease.fence };
}
