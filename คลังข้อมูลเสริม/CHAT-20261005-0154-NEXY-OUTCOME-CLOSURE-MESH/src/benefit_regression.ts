import { compareText, fingerprint64, hasDuplicates, isNonBlank, type CanonicalValue } from "./canonical.js";

export type BenefitDirection = "HIGHER" | "LOWER";

export interface BenefitAxis {
  readonly id: string;
  readonly direction: BenefitDirection;
  readonly critical: boolean;
  readonly minImprovement: number;
  readonly maxRegression: number;
}

export interface BenefitRegressionResult {
  readonly status: "BENEFICIAL" | "REJECT" | "INCONCLUSIVE" | "FREEZE";
  readonly improvedAxes: readonly string[];
  readonly regressedAxes: readonly string[];
  readonly missingAxes: readonly string[];
  readonly normalizedDelta: Readonly<Record<string, number>>;
  readonly reasons: readonly string[];
  readonly fingerprint: string;
}

export function judgeBenefitRegression(
  axes: readonly BenefitAxis[],
  baseline: Readonly<Record<string, number>>,
  candidate: Readonly<Record<string, number>>,
): BenefitRegressionResult {
  const normalizedAxes = [...axes].sort((a, b) => compareText(a.id, b.id));
  const validationReasons: string[] = [];
  const ids = normalizedAxes.map((axis) => axis.id);
  if (ids.some((id) => !isNonBlank(id))) validationReasons.push("BLANK_AXIS_ID");
  if (hasDuplicates(ids)) validationReasons.push("DUPLICATE_AXIS_ID");
  if (normalizedAxes.length === 0) validationReasons.push("NO_AXES");
  for (const axis of normalizedAxes) {
    if (axis.direction !== "HIGHER" && axis.direction !== "LOWER") validationReasons.push(`INVALID_DIRECTION:${axis.id}`);
    if (!Number.isInteger(axis.minImprovement) || axis.minImprovement <= 0) validationReasons.push(`INVALID_MIN_IMPROVEMENT:${axis.id}`);
    if (!Number.isInteger(axis.maxRegression) || axis.maxRegression < 0) validationReasons.push(`INVALID_MAX_REGRESSION:${axis.id}`);
  }

  const improvedAxes: string[] = [];
  const regressedAxes: string[] = [];
  const missingAxes: string[] = [];
  const normalizedDelta: Record<string, number> = {};
  const criticalRegressions: string[] = [];

  for (const axis of normalizedAxes) {
    const before = baseline[axis.id];
    const after = candidate[axis.id];
    if (before === undefined || after === undefined || !Number.isFinite(before) || !Number.isFinite(after)) {
      missingAxes.push(axis.id);
      continue;
    }
    const delta = axis.direction === "HIGHER" ? after - before : before - after;
    normalizedDelta[axis.id] = delta;
    if (delta >= axis.minImprovement) improvedAxes.push(axis.id);
    if (delta < -axis.maxRegression) {
      regressedAxes.push(axis.id);
      if (axis.critical) criticalRegressions.push(axis.id);
    }
  }

  let status: BenefitRegressionResult["status"];
  const reasons: string[] = [...validationReasons];
  if (validationReasons.length > 0) {
    status = "FREEZE";
  } else if (missingAxes.length > 0) {
    status = "INCONCLUSIVE";
    reasons.push(...missingAxes.map((id) => `MISSING_AXIS:${id}`));
  } else if (criticalRegressions.length > 0) {
    status = "REJECT";
    reasons.push(...criticalRegressions.map((id) => `CRITICAL_REGRESSION:${id}`));
  } else if (improvedAxes.length === 0) {
    status = "REJECT";
    reasons.push("NO_DECLARED_IMPROVEMENT");
  } else {
    status = "BENEFICIAL";
  }

  improvedAxes.sort(compareText);
  regressedAxes.sort(compareText);
  missingAxes.sort(compareText);
  const sortedReasons = [...new Set(reasons)].sort(compareText);
  const identity: CanonicalValue = {
    axes: normalizedAxes.map((axis) => ({
      id: axis.id,
      direction: axis.direction,
      critical: axis.critical,
      minImprovement: axis.minImprovement,
      maxRegression: axis.maxRegression,
    })),
    baseline: Object.fromEntries(ids.filter((id) => baseline[id] !== undefined).map((id) => [id, baseline[id]!])) as Record<string, number>,
    candidate: Object.fromEntries(ids.filter((id) => candidate[id] !== undefined).map((id) => [id, candidate[id]!])) as Record<string, number>,
    status,
    improvedAxes,
    regressedAxes,
    missingAxes,
    normalizedDelta,
    reasons: sortedReasons,
  };

  return {
    status,
    improvedAxes,
    regressedAxes,
    missingAxes,
    normalizedDelta,
    reasons: sortedReasons,
    fingerprint: fingerprint64(identity),
  };
}
