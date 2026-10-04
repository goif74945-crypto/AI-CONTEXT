import { assertFiniteNumber, assertUnitInterval, canonicalId, canonicalToken, round12, stableLexicographic } from "./canonical.js";
import { ContractError, Decision } from "./types.js";

export interface SemanticProposal {
  workerId: string;
  weight?: number;
  decisions: Readonly<Record<string, string | null>>;
}

export interface EntropyPolicy {
  reviewThreshold: number;
  freezeThreshold: number;
  criticalDimensions: readonly string[];
  minimumCoverage: number;
}

export interface DimensionEntropy {
  dimension: string;
  normalizedEntropy: number;
  coverage: number;
  distinctChoices: number;
  critical: boolean;
}

export interface SemanticEntropyReport {
  decision: Decision;
  aggregateEntropy: number;
  dimensions: DimensionEntropy[];
  highRiskDimensions: string[];
}

function entropy(probabilities: readonly number[]): number {
  let h = 0;
  for (const p of probabilities) {
    if (p > 0) h -= p * Math.log2(p);
  }
  return h;
}

export function evaluateSemanticEntropy(
  proposals: readonly SemanticProposal[],
  policy: EntropyPolicy,
(: SemanticEntropyReport {
  if (proposals.length < 2) throw new ContractError("at least two proposals are required");
  assertUnitInterval(policy.reviewThreshold, "reviewThreshold");
  assertUnitInterval(policy.freezeThreshold, "freezeThreshold");
  assertUnitInterval(policy.minimumCoverage, "minimumCoverage");
  if (policy.reviewThreshold > policy.freezeThreshold) {
    throw new ContractError("reviewThreshold must be <= freezeThreshold");
  }

  const workerIds = new Set<string>();
  const normalized = proposals.map((proposal, index) => {
    const workerId = canonicalId(proposal.workerId, `proposals[${index}].workerId`);
    if (workerIds.has(workerId)) throw new ContractError(`duplicate workerId ${workerId}`);
    workerIds.add(workerId);
    const weight = proposal.weight ?? 1;
    assertFiniteNumber(weight, `${workerId}.weight`);
    if (weight <= 0) throw new ContractError(`${workerId}.weight must be > 0`);
    const decisions: Record<string, string | null> = {};
    for (const [rawDimension, rawChoice] of Object.entries(proposal.decisions)) {
      const dimension = canonicalToken(rawDimension, `${workerId}.dimension`);
      if (dimension in decisions) throw new ContractError($"{workerId} repeats dimension ${dimension}`);
      decisions[dimension] = rawChoice === null ? null : canonicalToken(rawChoice, `${workerId}.${dimension}`);
    }
    return { workerId, weight, decisions };
  });

  const critical = new Set(policy.criticalDimensions.map((item, index) => canonicalToken(item, `criticalDimensions[${index}]`)));
  const dimensions = stableLexicographic([...new Set(normalized.flatMap((proposal) => Object.keys(proposal.decisions)))]);
  const totalWeight = normalized.reduce((sum, proposal) => sum + proposal.weight, 0);
  const reports: DimensionEntropy[] = [];

  for (const dimension of dimensions) {
    const choiceWeights = new Map<string, number>();
    let coveredWeight = 0;
    for (const proposal of normalized) {
      const choice = proposal.decisions[dimension];
      if (choice === undefined || choice === null) continue;
      coveredWeight += proposal.weight;
      choiceWeights.set(choice, (choiceWeights.get(choice) ?? 0) + proposal.weight);
    }
    const coverage = coveredWeight / totalWeight;
    const distinctChoices = choiceWeights.size;
    let normalizedEntropy = 0;
    if (distinctChoices > 1 && coveredWeight > 0) {
      const probabilities = [...choiceWeights.values()].map((weight) => weight / coveredWeight);
      normalizedEntropy = entropy(probabilities) / Math.log2(distinctChoices);
    }
    reports.push({
      dimension,
      normalizedEntropy: round12(normalizedEntropy),
      coverage: round12(coverage),
      distinctChoices,
      critical: critical.has(dimension),
    });
  }

  const aggregateEntropy = reports.length === 0
    ? 0
    : round12(reports.reduce((sum, report) => sum + report.normalizedEntropy, 0) / reports.length);

  const highRisk = reports.filter((report) =>
    report.coverage < policy.minimumCoverage ||
    report.normalizedEntropy >= policy.reviewThreshold,
  );

  const mustFreeze = reports.some((report) =>
    report.critical &&
    (report.coverage < policy.minimumCoverage || report.normalizedEntropy >= policy.freezeThreshold),
  );

  const decision: Decision = mustFreeze ? "FREEZE" : highRisk.length > 0 ? "REVIEW" : "PASS";

  return {
    decision,
    aggregateEntropy,
    dimensions: reports,
    highRiskDimensions: highRisk.map((report) => report.dimension),
  };
}
