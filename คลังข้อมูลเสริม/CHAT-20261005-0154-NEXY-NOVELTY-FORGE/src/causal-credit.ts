import { assertFiniteNumber, canonicalId, round12, stableLexicographic } from "./canonical.js";
import { ContractError } from "./types.js";

export interface OutcomeCreditInput {
  actionIds: readonly string[];
  coalitionValues: Readonly<Record<string, number>>;
  maxActions?: number;
}

export interface ActionCredit {
  actionId: string;
  contribution: number;
}

export interface OutcomeCreditReport {
  baseline: number;
  fullOutcome: number;
  totalDelta: number;
  credits: ActionCredit[];
  efficiencyResidual: number;
  interpretation: "COUNTERFACTUAL_CONTRIBUTION_NOT_CAUSAL_PROOF";
}

function factorial(n: number): number {
  let value = 1;
  for (let i = 2; i <= n; i += 1) value *= i;
  return value;
}

function keyFor(actions: readonly string[]): string {
  return stableLexicographic(actions).join("|");
}

export function enumerateCoalitionKeys(actionIds: readonly string[]): string[] {
  const sorted = stableLexicographic(actionIds);
  const count = 1 << sorted.length;
  const keys: string[] = [];
  for (let mask = 0; mask < count; mask += 1) {
    const members: string[] = [];
    for (let i = 0; i < sorted.length; i += 1) {
      if ((mask & (1 << i)) !== 0) members.push(sorted[i]!);
    }
    keys.push(keyFor(members));
  }
  return keys;
}

export function computeOutcomeCredits(input: OutcomeCreditInput): OutcomeCreditReport {
  const limit = input.maxActions ?? 10;
  if (!Number.isInteger(limit) || limit < 1 || limit > 20) {
    throw new ContractError("maxActions must be an integer between 1 and 20");
  }

  const ids = input.actionIds.map((id, index) => canonicalId(id, `actionIds[${index}]`));
  if (new Set(ids).size !== ids.length) throw new ContractError("actionIds must be unique");
  if (ids.length === 0) throw new ContractError("at least one actionId is required");
  if (ids.length > limit) throw new ContractError(`action count ${ids.length} exceeds maxActions ${limit}`);

  const sorted = stableLexicographic(ids);
  const requiredKeys = enumerateCoalitionKeys(sorted);
  const missing = requiredKeys.filter((key) => !(key in input.coalitionValues));
  if (missing.length > 0) {
    throw new ContractError(`coalitionValues is incomplete; missing ${missing.length} coalition(s)`, [
      { code: "MISSING_COALITIONS", message: missing.slice(0, 16).join(", ") || "<empty coalition>" },
    ]);
  }

  for (const key of requiredKeys) {
    assertFiniteNumber(input.coalitionValues[key]!, `coalitionValues[${JSON.stringify(key)}]`);
  }

  const n = sorted.length;
  const nFactorial = factorial(n);
  const credits: ActionCredit[] = [];

  for (const actionId of sorted) {
    const others = sorted.filter((id) => id !== actionId);
    let phi = 0;
    const coalitionCount = 1 << others.length;

    for (let mask = 0; mask < coalitionCount; mask += 1) {
      const coalition: string[] = [];
      for (let i = 0; i < others.length; i += 1) {
        if ((mask & (1 << i)) !== 0) coalition.push(others[i]!);
      }
      const withAction = [...coalition, actionId];
      const s = coalition.length;
      const weight = (factorial(s) * factorial(n - s - 1)) / nFactorial;
      const marginal = input.coalitionValues[keyFor(withAction)]! - input.coalitionValues[keyFor(coalition)]!;
      phi += weight * marginal;
    }
    credits.push({ actionId, contribution: round12(phi) });
  }

  const baseline = input.coalitionValues[""]!;
  const fullOutcome = input.coalitionValues[keyFor(sorted)]!;
  const totalDelta = round12(fullOutcome - baseline);
  const credited = credits.reduce((sum, item) => sum + item.contribution, 0);

  return {
    baseline,
    fullOutcome,
    totalDelta,
    credits,
    efficiencyResidual: round12(totalDelta - credited),
    interpretation: "COUNTERFACTUAL_CONTRIBUTION_NOT_CAUSAL_PROOF",
  };
}
