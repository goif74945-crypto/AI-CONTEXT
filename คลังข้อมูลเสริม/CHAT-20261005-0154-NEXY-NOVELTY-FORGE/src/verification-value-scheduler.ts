import { assertFiniteNumber, assertUnitInterval, canonicalId, round12, stableLexicographic } from "./canonical.js";
import { ContractError } from "./types.js";

export interface EvidenceOption {
  optionId: string;
  costUnits: number;
  expectedUncertaintyAfter: number;
  satisfiesRequiredClass: boolean;
}

export interface VerificationClaim {
  claimId: string;
  riskWeight: number;
  failureImpact: number;
  priorUncertainty: number;
  mustVerify: boolean;
  options: readonly EvidenceOption[];
}

export interface ScheduledVerification {
  claimId: string;
  optionId: string;
  costUnits: number;
  expectedRiskReduction: number;
  mandatory: boolean;
}

export interface VerificationSchedule {
  selected: ScheduledVerification[];
  totalCostUnits: number;
  budgetUnits: number;
  totalExpectedRiskReduction: number;
  uncoveredMandatoryClaims: string[];
  status: "PASS" | "BLOCKED";
}

interface Candidate {
  claimId: string;
  optionId: string;
  costUnits: number;
  score: number;
  mandatory: boolean;
}

function candidateFor(claim: VerificationClaim, option: EvidenceOption): Candidate {
  const uncertaintyDrop = claim.priorUncertainty - option.expectedUncertaintyAfter;
  const score = claim.riskWeight * claim.failureImpact * Math.max(0, uncertaintyDrop);
  return {
    claimId: claim.claimId,
    optionId: option.optionId,
    costUnits: option.costUnits,
    score: round12(score),
    mandatory: claim.mustVerify,
  };
}

function validateClaim(claim: VerificationClaim, index: number): VerificationClaim {
  const claimId = canonicalId(claim.claimId, `claims[${index}].claimId`);
  assertFiniteNumber(claim.riskWeight, `claims[${index}].riskWeight`);
  assertFiniteNumber(claim.failureImpact, `claims[${index}].failureImpact`);
  if (claim.riskWeight < 0 || claim.failureImpact < 0) throw new ContractError("riskWeight and failureImpact must be >= 0");
  assertUnitInterval(claim.priorUncertainty, `claims[${index}].priorUncertainty`);
  if (claim.options.length === 0) throw new ContractError(`${claimId} must provide at least one evidence option`);

  const optionIds = new Set<string>();
  const options = claim.options.map((option, optionIndex) => {
    const optionId = canonicalId(option.optionId, `claims[${index}].options[${optionIndex}].optionId`);
    if (optionIds.has(optionId)) throw new ContractError(`${claimId} has duplicate optionId ${optionId}`);
    optionIds.add(optionId);
    if (!Number.isInteger(option.costUnits) || option.costUnits <= 0) throw new ContractError(`${claimId}/${optionId} costUnits must be a positive integer`);
    assertUnitInterval(option.expectedUncertaintyAfter, `${claimId}/${optionId}.expectedUncertaintyAfter`);
    if (option.expectedUncertaintyAfter > claim.priorUncertainty) {
      throw new ContractError(`${claimId}/${optionId} cannot increase expected uncertainty`);
    }
    return { ...option, optionId };
  });
  return { ...claim, claimId, options };
}

function comparePlan(a: Candidate[], b: Candidate[]): number {
  const scoreA = a.reduce((sum, item) => sum + item.score, 0);
  const scoreB = b.reduce((sum, item) => sum + item.score, 0);
  if (Math.abs(scoreA - scoreB) > 1e-12) return scoreA > scoreB ? 1 : -1;
  const costA = a.reduce((sum, item) => sum + item.costUnits, 0);
  const costB = b.reduce((sum, item) => sum + item.costUnits, 0);
  if (costA !== costB) return costA < costB ? 1 : -1;
  const keyA = a.map((item) => `${item.claimId}/${item.optionId}`).sort().join("|");
  const keyB = b.map((item) => `${item.claimId}/${item.optionId}`).sort().join("|");
  return keyA.localeCompare(keyB, "en") <= 0 ? 1 : -1;
}

export function scheduleVerification(claimsInput: readonly VerificationClaim[], budgetUnits: number): VerificationSchedule {
  if (!Number.isInteger(budgetUnits) || budgetUnits < 0) throw new ContractError("budgetUnits must be a non-negative integer");
  const claims = claimsInput.map(validateClaim);
  const ids = claims.map((claim) => claim.claimId);
  if (new Set(ids).size !== ids.length) throw new ContractError("claimIds must be unique");

  const mandatory: Candidate[] = [];
  const uncoveredMandatoryClaims: string[] = [];
  let mandatoryCost = 0;

  for (const claim of claims.filter((item) => item.mustVerify)) {
    const valid = claim.options.filter((option) => option.satisfiesRequiredClass);
    if (valid.length === 0) {
      uncoveredMandatoryClaims.push(claim.claimId);
      continue;
    }
    const candidates = valid.map((option) => candidateFor(claim, option));
    candidates.sort((a, b) => a.costUnits - b.costUnits || b.score - a.score || a.optionId.localeCompare(b.optionId, "en"));
    const selected = candidates[0]!;
    mandatory.push(selected);
    mandatoryCost += selected.costUnits;
  }

  if (uncoveredMandatoryClaims.length > 0 || mandatoryCost > budgetUnits) {
    return {
      selected: mandatory.map((item) => ({ ...item, expectedRiskReduction: item.score })),
      totalCostUnits: mandatoryCost,
      budgetUnits,
      totalExpectedRiskReduction: round12(mandatory.reduce((sum, item) => sum + item.score, 0)),
      uncoveredMandatoryClaims: stableLexicographic(uncoveredMandatoryClaims),
      status: "BLOCKED",
    };
  }

  const remainingBudget = budgetUnits - mandatoryCost;
  const optionalClaims = claims.filter((claim) => !claim.mustVerify);
  const dp: Candidate[][] = Array.from({ length: remainingBudget + 1 }, () => []);
  const reachable = new Array<boolean>(remainingBudget + 1).fill(false);
  reachable[0] = true;

  for (const claim of optionalClaims) {
    const previousPlans = dp.map((plan) => [...plan]);
    const previousReachable = [...reachable];
    for (let cost = 0; cost <= remainingBudget; cost += 1) {
      if (!previousReachable[cost]) continue;
      for (const option of claim.options) {
        const candidate = candidateFor(claim, option);
        const nextCost = cost + candidate.costUnits;
        if (nextCost > remainingBudget) continue;
        const nextPlan = [...previousPlans[cost]!, candidate];
        if (!reachable[nextCost] || comparePlan(nextPlan, dp[nextCost]!) > 0) {
          dp[nextCost] = nextPlan;
          reachable[nextCost] = true;
        }
      }
    }
  }

  let best: Candidate[] = [];
  for (let cost = 0; cost <= remainingBudget; cost += 1) {
    if (reachable[cost] && comparePlan(dp[cost]!, best) > 0) best = dp[cost]!;
  }

  const all = [...mandatory, ...best].sort((a, b) => a.claimId.localeCompare(b.claimId, "en"));
  return {
    selected: all.map((item) => ({
      claimId: item.claimId,
      optionId: item.optionId,
      costUnits: item.costUnits,
      expectedRiskReduction: item.score,
      mandatory: item.mandatory,
    })),
    totalCostUnits: all.reduce((sum, item) => sum + item.costUnits, 0),
    budgetUnits,
    totalExpectedRiskReduction: round12(all.reduce((sum, item) => sum + item.score, 0)),
    uncoveredMandatoryClaims: [],
    status: "PASS",
  };
}
