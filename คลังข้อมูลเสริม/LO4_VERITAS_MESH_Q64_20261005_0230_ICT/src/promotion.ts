import { createHash } from "node:crypto";
import { UnitQ64 } from "./q64.ts";
import { CONCEPT_IDS, evaluateAll, type ConceptId } from "./models.ts";
import { frameToRaw, type SignalFrame } from "./signals.ts";

export type PromotionStatus = "REJECT" | "QUARANTINE" | "ELIGIBLE_FOR_PROMOTION_REVIEW";

export interface GateThreshold {
  concept: ConceptId;
  minimum: UnitQ64;
}

export const MANDATORY_GATES: readonly GateThreshold[] = [
  { concept: "requirement-lock", minimum: UnitQ64.fromDecimal("0.80") },
  { concept: "evidence-reliability", minimum: UnitQ64.fromDecimal("0.75") },
  { concept: "canon-compatibility", minimum: UnitQ64.fromDecimal("0.85") },
  { concept: "regression-containment", minimum: UnitQ64.fromDecimal("0.80") },
  { concept: "reproducibility", minimum: UnitQ64.fromDecimal("0.95") },
  { concept: "safety-utility-balance", minimum: UnitQ64.fromDecimal("0.80") },
  { concept: "promotion-readiness", minimum: UnitQ64.fromDecimal("0.85") }
] as const;

const OVERALL_ELIGIBLE = UnitQ64.fromDecimal("0.85");
const OVERALL_QUARANTINE = UnitQ64.fromDecimal("0.65");

// Catastrophic weaknesses are never allowed to hide behind a strong average.
// These are deliberately stricter than ordinary quarantine behavior.
const CRITICAL_REJECT_GATES: readonly GateThreshold[] = [
  { concept: "safety-utility-balance", minimum: UnitQ64.fromDecimal("0.50") },
  { concept: "reproducibility", minimum: UnitQ64.fromDecimal("0.80") },
  { concept: "canon-compatibility", minimum: UnitQ64.fromDecimal("0.60") },
  { concept: "requirement-lock", minimum: UnitQ64.fromDecimal("0.50") }
] as const;

export interface PromotionDecision {
  engineVersion: "lo4-veritas-mesh/0.1.0";
  authority: "NON_CANONICAL_LO4_ONLY";
  status: PromotionStatus;
  overall: UnitQ64;
  scores: Record<ConceptId, UnitQ64>;
  failedMandatoryGates: readonly ConceptId[];
  receiptSha256: string;
  canonicalPromotionPerformed: false;
}

function stablePayload(frame: SignalFrame, scores: Record<ConceptId, UnitQ64>, status: PromotionStatus, overall: UnitQ64): string {
  const rawFrame = frameToRaw(frame);
  const signalKeys = Object.keys(rawFrame).sort() as (keyof typeof rawFrame)[];
  const signals = signalKeys.map((key) => [key, rawFrame[key]]);
  const scoreRows = CONCEPT_IDS.map((id) => [id, scores[id].toRawString()]);
  return JSON.stringify({
    engineVersion: "lo4-veritas-mesh/0.1.0",
    authority: "NON_CANONICAL_LO4_ONLY",
    status,
    overall: overall.toRawString(),
    signals,
    scores: scoreRows,
    canonicalPromotionPerformed: false
  });
}

export function decidePromotion(frame: SignalFrame): PromotionDecision {
  const scores = evaluateAll(frame);
  const overall = UnitQ64.weightedAverage(CONCEPT_IDS.map((id) => ({ value: scores[id], weight: 1n })));
  const failedMandatoryGates = MANDATORY_GATES
    .filter((gate) => scores[gate.concept].raw < gate.minimum.raw)
    .map((gate) => gate.concept);

  const failedCriticalGate = CRITICAL_REJECT_GATES.some(
    (gate) => scores[gate.concept].raw < gate.minimum.raw
  );

  let status: PromotionStatus;
  if (failedCriticalGate) {
    status = "REJECT";
  } else if (failedMandatoryGates.length === 0 && overall.raw >= OVERALL_ELIGIBLE.raw) {
    status = "ELIGIBLE_FOR_PROMOTION_REVIEW";
  } else if (overall.raw >= OVERALL_QUARANTINE.raw) {
    status = "QUARANTINE";
  } else {
    status = "REJECT";
  }

  const receiptSha256 = createHash("sha256").update(stablePayload(frame, scores, status, overall)).digest("hex");
  return {
    engineVersion: "lo4-veritas-mesh/0.1.0",
    authority: "NON_CANONICAL_LO4_ONLY",
    status,
    overall,
    scores,
    failedMandatoryGates,
    receiptSha256,
    canonicalPromotionPerformed: false
  };
}

export function decisionToPortableJson(decision: PromotionDecision): string {
  return JSON.stringify({
    engineVersion: decision.engineVersion,
    authority: decision.authority,
    status: decision.status,
    overallRawQ64_64: decision.overall.toRawString(),
    scoresRawQ64_64: Object.fromEntries(CONCEPT_IDS.map((id) => [id, decision.scores[id].toRawString()])),
    failedMandatoryGates: [...decision.failedMandatoryGates],
    receiptSha256: decision.receiptSha256,
    canonicalPromotionPerformed: decision.canonicalPromotionPerformed
  }, null, 2);
}
