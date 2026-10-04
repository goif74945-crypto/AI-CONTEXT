import { Q64 } from "./q64";
import { ForgeError, canonicalStrings, nonEmpty } from "./core";
export interface ConstraintNegationExperiment {
  readonly id: string;
  readonly hypothesisId: string;
  readonly negatedConstraint: string;
  readonly mutation: string;
  readonly expectedObservation: "FALSIFY_OR_SURVIVE";
}

export function constraintNegationExperimentPlanner(
  hypothesisId: string,
  constraints: readonly string[]
): readonly ConstraintNegationExperiment[] {
  const hid = nonEmpty(hypothesisId, "hypothesis id");
  const normalized = canonicalStrings(constraints, "constraint");
  return Object.freeze(normalized.map((constraint, index) => Object.freeze({
    id: `CNEP-${hid}-${String(index + 1).padStart(4, "0")}`,
    hypothesisId: hid,
    negatedConstraint: constraint,
    mutation: `negate:${constraint}`,
    expectedObservation: "FALSIFY_OR_SURVIVE" as const
  })));
}

export interface BoundaryProbe {
  readonly id: string;
  readonly metric: string;
  readonly position: "BELOW_MIN" | "AT_MIN" | "INSIDE_MIN" | "INSIDE_MAX" | "AT_MAX" | "ABOVE_MAX";
  readonly value: Q64;
}

export function boundaryConditionProbePlanner(metric: string, minimum: Q64, maximum: Q64): readonly BoundaryProbe[] {
  const name = nonEmpty(metric, "metric");
  if (minimum.compare(maximum) > 0) throw new ForgeError("minimum exceeds maximum");
  if (minimum.raw === Q64.MIN_RAW || maximum.raw === Q64.MAX_RAW) {
    throw new ForgeError("cannot create outside-boundary probes at signed-128 edge");
  }
  const insideMinRaw = minimum.raw < maximum.raw ? minimum.raw + 1n : minimum.raw;
  const insideMaxRaw = maximum.raw > minimum.raw ? maximum.raw - 1n : maximum.raw;
  const values: readonly [BoundaryProbe["position"], bigint][] = [
    ["BELOW_MIN", minimum.raw - 1n],
    ["AT_MIN", minimum.raw],
    ["INSIDE_MIN", insideMinRaw],
    ["INSIDE_MAX", insideMaxRaw],
    ["AT_MAX", maximum.raw],
    ["ABOVE_MAX", maximum.raw + 1n]
  ];
  return Object.freeze(values.map(([position, raw], index) => Object.freeze({
    id: `BCPP-${name}-${String(index + 1).padStart(2, "0")}`,
    metric: name,
    position,
    value: Q64.fromRaw(raw)
  })));
}

export interface FaultExperiment {
  readonly id: string;
  readonly fault: string;
  readonly injection: string;
  readonly requiredOutcome: "EXPLICIT_CONTAIN_OR_FREEZE";
}

export function faultInjectionExperimentPlanner(faults: readonly string[]): readonly FaultExperiment[] {
  const normalized = canonicalStrings(faults, "fault");
  return Object.freeze(normalized.map((fault, index) => Object.freeze({
    id: `FIEP-${String(index + 1).padStart(4, "0")}-${fault}`,
    fault,
    injection: `inject:${fault}`,
    requiredOutcome: "EXPLICIT_CONTAIN_OR_FREEZE" as const
  })));
}

export interface AssumptionInput { readonly id: string; readonly statement: string; }
export interface AssumptionKillExperiment {
  readonly id: string;
  readonly assumptionId: string;
  readonly violatedAssumption: string;
  readonly expectedIfAssumptionFalse: "HYPOTHESIS_AT_RISK";
}

export function assumptionKillExperimentPlanner(assumptions: readonly AssumptionInput[]): readonly AssumptionKillExperiment[] {
  if (assumptions.length === 0) throw new ForgeError("at least one assumption is required");
  const normalized = assumptions.map((assumption) => ({
    id: nonEmpty(assumption.id, "assumption id"),
    statement: nonEmpty(assumption.statement, "assumption statement")
  })).sort((a, b) => a.id.localeCompare(b.id));
  const seen = new Set<string>();
  for (const assumption of normalized) {
    if (seen.has(assumption.id)) throw new ForgeError(`duplicate assumption id: ${assumption.id}`);
    seen.add(assumption.id);
  }
  return Object.freeze(normalized.map((assumption) => Object.freeze({
    id: `AKEP-${assumption.id}`,
    assumptionId: assumption.id,
    violatedAssumption: assumption.statement,
    expectedIfAssumptionFalse: "HYPOTHESIS_AT_RISK" as const
  })));
}

