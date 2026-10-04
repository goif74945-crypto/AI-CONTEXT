export type Operator = "<" | "<=" | ">" | ">=" | "==";

export interface Constraint {
  readonly name: string;
  readonly actual: number;
  readonly operator: Operator;
  readonly limit: number;
  readonly scale?: number;
  readonly requiredMargin?: number;
}

export interface ConstraintResult {
  readonly name: string;
  readonly legal: boolean;
  readonly rawSlack: number;
  readonly normalizedMargin: number;
  readonly status: "VIOLATION" | "FRAGILE_PASS" | "ROBUST_PASS";
}

export interface DecisionMarginReport {
  readonly results: readonly ConstraintResult[];
  readonly minimumMargin: number;
  readonly releaseStatus: "FREEZE" | "REVERIFY" | "RELEASE";
  readonly reasons: readonly string[];
}

export function evaluateConstraints(constraints: readonly Constraint[]): DecisionMarginReport {
  if (constraints.length === 0) throw new Error("at least one constraint is required");
  const names = new Set<string>();
  const results = constraints.map((c): ConstraintResult => {
    if (!c.name || names.has(c.name)) throw new Error("constraint names must be unique and non-empty");
    names.add(c.name);
    const scale = c.scale ?? 1;
    const required = c.requiredMargin ?? 0;
    for (const [name, value] of Object.entries({ actual: c.actual, limit: c.limit, scale, required })) {
      if (!Number.isFinite(value)) throw new Error(`${name} must be finite`);
    }
    if (scale <= 0) throw new Error("scale must be > 0");
    if (required < 0) throw new Error("requiredMargin must be >= 0");

    let legal: boolean;
    let slack: number;
    switch (c.operator) {
      case "<=": legal = c.actual <= c.limit; slack = c.limit - c.actual; break;
      case "<": legal = c.actual < c.limit; slack = c.limit - c.actual; break;
      case ">=": legal = c.actual >= c.limit; slack = c.actual - c.limit; break;
      case ">": legal = c.actual > c.limit; slack = c.actual - c.limit; break;
      case "==": legal = c.actual === c.limit; slack = legal ? 0 : -Math.abs(c.actual - c.limit); break;
    }
    const margin = slack / scale;
    const status: ConstraintResult["status"] = !legal
      ? "VIOLATION"
      : margin < required
        ? "FRAGILE_PASS"
        : "ROBUST_PASS";
    return Object.freeze({ name: c.name, legal, rawSlack: slack, normalizedMargin: margin, status });
  });

  const reasons: string[] = [];
  let releaseStatus: DecisionMarginReport["releaseStatus"];
  if (results.some((r) => r.status === "VIOLATION")) {
    releaseStatus = "FREEZE";
    for (const r of results) if (r.status === "VIOLATION") reasons.push(`violation:${r.name}`);
  } else if (results.some((r) => r.status === "FRAGILE_PASS")) {
    releaseStatus = "REVERIFY";
    for (const r of results) if (r.status === "FRAGILE_PASS") reasons.push(`fragile:${r.name}`);
  } else {
    releaseStatus = "RELEASE";
  }
  return Object.freeze({
    results: Object.freeze(results),
    minimumMargin: Math.min(...results.map((r) => r.normalizedMargin)),
    releaseStatus,
    reasons: Object.freeze(reasons),
  });
}
