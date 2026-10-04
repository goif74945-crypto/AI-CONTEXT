import { compareText, fingerprint64, hasDuplicates, isNonBlank, type CanonicalValue } from "./canonical.js";

export type ObligationStatus = "PASS" | "FAIL" | "PENDING" | "BLOCKED" | "UNKNOWN";
export type ProgressAggregate = "COMPLETE" | "INCOMPLETE" | "BLOCKED" | "NOT_VERIFIED" | "FREEZE";

export interface ProgressObligation {
  readonly id: string;
  readonly status: ObligationStatus;
}

export interface ProgressSummary {
  readonly aggregate: ProgressAggregate;
  readonly completeClaimAllowed: boolean;
  readonly passRatioBps: number | null;
  readonly byStatus: Readonly<Record<ObligationStatus, readonly string[]>>;
  readonly reasons: readonly string[];
  readonly fingerprint: string;
}

const STATUSES: readonly ObligationStatus[] = ["PASS", "FAIL", "PENDING", "BLOCKED", "UNKNOWN"];

export function summarizeProgress(obligations: readonly ProgressObligation[]): ProgressSummary {
  const normalized = obligations
    .map((obligation) => ({ id: obligation.id, status: obligation.status }))
    .sort((a, b) => compareText(a.id, b.id));

  const reasons: string[] = [];
  const ids = normalized.map((obligation) => obligation.id);
  if (ids.some((id) => !isNonBlank(id))) reasons.push("BLANK_OBLIGATION_ID");
  if (hasDuplicates(ids)) reasons.push("DUPLICATE_OBLIGATION_ID");
  if (normalized.some((obligation) => !STATUSES.includes(obligation.status))) reasons.push("INVALID_OBLIGATION_STATUS");

  const byStatus: Record<ObligationStatus, string[]> = {
    PASS: [],
    FAIL: [],
    PENDING: [],
    BLOCKED: [],
    UNKNOWN: [],
  };
  for (const obligation of normalized) {
    if (STATUSES.includes(obligation.status)) byStatus[obligation.status].push(obligation.id);
  }
  for (const status of STATUSES) byStatus[status].sort(compareText);

  let aggregate: ProgressAggregate;
  if (reasons.length > 0) aggregate = "FREEZE";
  else if (normalized.length === 0) aggregate = "NOT_VERIFIED";
  else if (byStatus.BLOCKED.length > 0) aggregate = "BLOCKED";
  else if (byStatus.UNKNOWN.length > 0) aggregate = "NOT_VERIFIED";
  else if (byStatus.FAIL.length > 0 || byStatus.PENDING.length > 0) aggregate = "INCOMPLETE";
  else aggregate = "COMPLETE";

  const passRatioBps = normalized.length === 0 ? null : Math.floor((byStatus.PASS.length * 10_000) / normalized.length);
  const completeClaimAllowed = aggregate === "COMPLETE";
  if (!completeClaimAllowed && reasons.length === 0) reasons.push(`AGGREGATE:${aggregate}`);
  const sortedReasons = [...reasons].sort(compareText);

  const identity: CanonicalValue = {
    obligations: normalized.map((obligation) => ({ id: obligation.id, status: obligation.status })),
    aggregate,
    completeClaimAllowed,
    passRatioBps,
    byStatus: {
      PASS: byStatus.PASS,
      FAIL: byStatus.FAIL,
      PENDING: byStatus.PENDING,
      BLOCKED: byStatus.BLOCKED,
      UNKNOWN: byStatus.UNKNOWN,
    },
    reasons: sortedReasons,
  };

  return {
    aggregate,
    completeClaimAllowed,
    passRatioBps,
    byStatus,
    reasons: sortedReasons,
    fingerprint: fingerprint64(identity),
  };
}
