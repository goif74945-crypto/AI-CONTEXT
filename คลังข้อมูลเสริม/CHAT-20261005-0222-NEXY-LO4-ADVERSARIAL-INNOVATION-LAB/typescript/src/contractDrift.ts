export interface TaskContract {
  readonly authorizedScope: readonly string[];
  readonly successInvariants: readonly string[];
  readonly forbiddenActions: readonly string[];
  readonly assumptions: readonly string[];
  readonly requiredEvidence: readonly string[];
}

export interface ContractDriftPolicy {
  readonly maxTotalCost: number;
  readonly blockUnapprovedScopeExpansion: boolean;
  readonly blockUnapprovedInvariantWeakening: boolean;
  readonly blockUnapprovedForbiddenWeakening: boolean;
  readonly blockUnapprovedAssumptionInjection: boolean;
  readonly blockUnapprovedEvidenceWeakening: boolean;
}

export interface DriftEvent {
  readonly eventId: string;
  readonly kind: string;
  readonly item: string;
  readonly cost: number;
  readonly approved: boolean;
}

export interface ContractDriftReport {
  readonly events: readonly DriftEvent[];
  readonly totalCost: number;
  readonly status: "PASS" | "FREEZE";
  readonly reasons: readonly string[];
}

export const DEFAULT_CONTRACT_DRIFT_POLICY: ContractDriftPolicy = Object.freeze({
  maxTotalCost: 3,
  blockUnapprovedScopeExpansion: true,
  blockUnapprovedInvariantWeakening: true,
  blockUnapprovedForbiddenWeakening: true,
  blockUnapprovedAssumptionInjection: true,
  blockUnapprovedEvidenceWeakening: true,
});

function asSet(values: readonly string[], name: string): Set<string> {
  if (!Array.isArray(values) || values.some((x) => typeof x !== "string" || x.length === 0)) {
    throw new Error(`${name} must contain non-empty strings`);
  }
  return new Set(values);
}

export function analyzeContractDrift(
  before: TaskContract,
  after: TaskContract,
  approvedEventIds: readonly string[] = [],
  policy: ContractDriftPolicy = DEFAULT_CONTRACT_DRIFT_POLICY,
): ContractDriftReport {
  if (!Number.isInteger(policy.maxTotalCost) || policy.maxTotalCost < 0) throw new Error("maxTotalCost must be integer >= 0");
  const approved = new Set(approvedEventIds);
  const events: DriftEvent[] = [];
  const push = (kind: string, item: string, cost: number): void => {
    const eventId = `${kind}:${item}`;
    events.push(Object.freeze({ eventId, kind, item, cost, approved: approved.has(eventId) }));
  };
  const diff = (a: Set<string>, b: Set<string>): string[] => [...a].filter((x) => !b.has(x)).sort();

  const bScope = asSet(before.authorizedScope, "authorizedScope");
  const aScope = asSet(after.authorizedScope, "authorizedScope");
  const bInv = asSet(before.successInvariants, "successInvariants");
  const aInv = asSet(after.successInvariants, "successInvariants");
  const bForbid = asSet(before.forbiddenActions, "forbiddenActions");
  const aForbid = asSet(after.forbiddenActions, "forbiddenActions");
  const bAssume = asSet(before.assumptions, "assumptions");
  const aAssume = asSet(after.assumptions, "assumptions");
  const bEvidence = asSet(before.requiredEvidence, "requiredEvidence");
  const aEvidence = asSet(after.requiredEvidence, "requiredEvidence");

  for (const item of diff(aScope, bScope)) push("scope_expansion", item, 8);
  for (const item of diff(bScope, aScope)) push("scope_narrowing", item, 1);
  for (const item of diff(bInv, aInv)) push("invariant_removed", item, 10);
  for (const item of diff(bForbid, aForbid)) push("forbidden_action_removed", item, 12);
  for (const item of diff(aAssume, bAssume)) push("assumption_added", item, 7);
  for (const item of diff(bEvidence, aEvidence)) push("required_evidence_removed", item, 9);

  const reasons: string[] = [];
  for (const event of events) {
    if (event.approved) continue;
    if (event.kind === "scope_expansion" && policy.blockUnapprovedScopeExpansion) reasons.push(event.eventId);
    if (event.kind === "invariant_removed" && policy.blockUnapprovedInvariantWeakening) reasons.push(event.eventId);
    if (event.kind === "forbidden_action_removed" && policy.blockUnapprovedForbiddenWeakening) reasons.push(event.eventId);
    if (event.kind === "assumption_added" && policy.blockUnapprovedAssumptionInjection) reasons.push(event.eventId);
    if (event.kind === "required_evidence_removed" && policy.blockUnapprovedEvidenceWeakening) reasons.push(event.eventId);
  }
  const totalCost = events.filter((e) => !e.approved).reduce((sum, e) => sum + e.cost, 0);
  if (totalCost > policy.maxTotalCost) reasons.push("drift_budget_exceeded");
  const uniqueReasons = [...new Set(reasons)];
  return Object.freeze({
    events: Object.freeze(events),
    totalCost,
    status: uniqueReasons.length === 0 ? "PASS" : "FREEZE",
    reasons: Object.freeze(uniqueReasons),
  });
}
