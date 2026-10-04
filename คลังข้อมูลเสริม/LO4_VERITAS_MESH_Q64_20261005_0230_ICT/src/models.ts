import { UnitQ64 } from "./q64.ts";
import type { SignalFrame } from "./signals.ts";

export const CONCEPT_IDS = [
  "requirement-lock",
  "evidence-reliability",
  "contradiction-resilience",
  "scope-integrity",
  "canon-compatibility",
  "regression-containment",
  "failure-visibility",
  "reproducibility",
  "safety-utility-balance",
  "novelty-discipline",
  "assumption-firewall",
  "dependency-survivability",
  "blast-radius-control",
  "agent-consensus-quality",
  "test-priority-fitness",
  "promotion-readiness",
  "user-value-preservation",
  "quarantine-readiness",
  "uncertainty-burndown",
  "future-adaptability"
] as const;

export type ConceptId = (typeof CONCEPT_IDS)[number];

const avg = (...pairs: readonly [UnitQ64, bigint][]): UnitQ64 =>
  UnitQ64.weightedAverage(pairs.map(([value, weight]) => ({ value, weight })));

const product = (...values: readonly UnitQ64[]): UnitQ64 => UnitQ64.product(values);

export function evaluateConcept(id: ConceptId, s: SignalFrame): UnitQ64 {
  switch (id) {
    case "requirement-lock":
      return avg([s.requirementClarity, 5n], [s.assumptionRatio.complement(), 3n], [s.canonAlignment, 2n]);
    case "evidence-reliability":
      return avg([product(s.evidenceCoverage, s.evidenceFreshness), 5n], [s.sourceDiversity, 2n], [s.provenanceCompleteness, 3n]);
    case "contradiction-resilience":
      return avg([product(s.contradictionPressure, s.agentDisagreement).complement(), 6n], [s.failureObservability, 2n], [s.evidenceCoverage, 2n]);
    case "scope-integrity":
      return avg([s.scopeDistance.complement(), 6n], [s.changeSurface.complement(), 2n], [s.requirementClarity, 2n]);
    case "canon-compatibility":
      return avg([product(s.canonAlignment, s.interfaceCompatibility), 7n], [s.deterministicReproducibility, 3n]);
    case "regression-containment":
      return avg([s.regressionRisk.complement(), 5n], [s.reversibility, 2n], [s.rollbackReadiness, 3n]);
    case "failure-visibility":
      return avg([s.failureObservability, 5n], [s.provenanceCompleteness, 3n], [s.testCoverage, 2n]);
    case "reproducibility":
      return avg([s.deterministicReproducibility, 7n], [s.dependencyStability, 2n], [s.provenanceCompleteness, 1n]);
    case "safety-utility-balance": {
      const hardFloor = s.safetyMargin.min(s.userValue);
      return avg([hardFloor, 6n], [product(s.safetyMargin, s.userValue), 4n]);
    }
    case "novelty-discipline":
      return avg([s.novelty, 3n], [s.uncertainty.complement(), 3n], [s.scopeDistance.complement(), 2n], [s.evidenceCoverage, 2n]);
    case "assumption-firewall":
      return avg([s.assumptionRatio.complement(), 6n], [s.evidenceCoverage, 2n], [s.provenanceCompleteness, 2n]);
    case "dependency-survivability":
      return avg([s.dependencyStability, 5n], [s.rollbackReadiness, 2n], [s.deterministicReproducibility, 3n]);
    case "blast-radius-control":
      return avg([s.changeSurface.complement(), 5n], [s.reversibility, 3n], [s.rollbackReadiness, 2n]);
    case "agent-consensus-quality": {
      const consensus = s.agentDisagreement.complement();
      const falseConsensusGuard = avg([s.sourceDiversity, 2n], [s.evidenceCoverage, 3n], [s.contradictionPressure.complement(), 2n]);
      return avg([consensus, 3n], [falseConsensusGuard, 7n]);
    }
    case "test-priority-fitness":
      return avg([s.testCoverage, 5n], [s.regressionRisk.complement(), 2n], [s.failureObservability, 3n]);
    case "promotion-readiness": {
      const hard = product(s.canonAlignment, s.safetyMargin, s.deterministicReproducibility);
      return avg([hard, 5n], [s.testCoverage, 2n], [s.evidenceCoverage, 2n], [s.reversibility, 1n]);
    }
    case "user-value-preservation":
      return avg([product(s.userValue, s.requirementClarity), 6n], [s.safetyMargin, 2n], [s.reversibility, 2n]);
    case "quarantine-readiness":
      return avg([s.rollbackReadiness, 4n], [s.failureObservability, 3n], [s.reversibility, 3n]);
    case "uncertainty-burndown":
      return avg([s.uncertainty.complement(), 5n], [product(s.evidenceCoverage, s.evidenceFreshness), 3n], [s.assumptionRatio.complement(), 2n]);
    case "future-adaptability":
      return avg([s.interfaceCompatibility, 4n], [s.dependencyStability, 3n], [s.reversibility, 2n], [s.novelty, 1n]);
  }
}

export function evaluateAll(frame: SignalFrame): Record<ConceptId, UnitQ64> {
  const out = {} as Record<ConceptId, UnitQ64>;
  for (const id of CONCEPT_IDS) out[id] = evaluateConcept(id, frame);
  return out;
}
