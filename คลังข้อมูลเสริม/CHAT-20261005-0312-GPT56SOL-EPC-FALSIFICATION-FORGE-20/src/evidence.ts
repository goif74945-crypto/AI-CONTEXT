import { Q64, q64Unit } from "./q64";
import type { AdvisoryAuthority } from "./core";
import { ForgeError, nonEmpty } from "./core";
export interface EvidenceChoice { readonly id: string; readonly discrimination: Q64; readonly cost: Q64; }

export function discriminatingEvidenceSelector(choices: readonly EvidenceChoice[]): EvidenceChoice {
  if (choices.length === 0) throw new ForgeError("at least one evidence choice is required");
  const normalized = choices.map((choice) => {
    const id = nonEmpty(choice.id, "evidence id");
    q64Unit(choice.discrimination, "discrimination");
    if (choice.cost.raw <= 0n) throw new ForgeError("evidence cost must be positive");
    return { id, discrimination: choice.discrimination, cost: choice.cost };
  });
  normalized.sort((a, b) => {
    // Compare a.discrimination/a.cost vs b.discrimination/b.cost exactly by cross multiplication.
    const left = a.discrimination.raw * b.cost.raw;
    const right = b.discrimination.raw * a.cost.raw;
    if (left > right) return -1;
    if (left < right) return 1;
    return a.id.localeCompare(b.id);
  });
  const best = normalized[0];
  if (best === undefined) throw new ForgeError("internal empty evidence set");
  return Object.freeze(best);
}

export interface OracleInput { readonly id: string; readonly root: string; }
export interface OraclePair { readonly left: string; readonly right: string; readonly purpose: "DISAGREEMENT_PROBE"; }
export interface OraclePlan { readonly independentRoots: bigint; readonly pairs: readonly OraclePair[]; }

export function oracleTriangulationPlanner(oracles: readonly OracleInput[]): OraclePlan {
  if (oracles.length < 2) throw new ForgeError("at least two oracles are required");
  const normalized = oracles.map((oracle) => ({
    id: nonEmpty(oracle.id, "oracle id"),
    root: nonEmpty(oracle.root, "oracle root")
  })).sort((a, b) => a.id.localeCompare(b.id));
  const roots = new Set(normalized.map((x) => x.root));
  if (roots.size < 2) throw new ForgeError("oracles are not independent");
  const pairs: OraclePair[] = [];
  for (let i = 0; i < normalized.length; i += 1) {
    const left = normalized[i];
    if (left === undefined) continue;
    for (let j = i + 1; j < normalized.length; j += 1) {
      const right = normalized[j];
      if (right !== undefined && left.root !== right.root) {
        pairs.push(Object.freeze({left:left.id,right:right.id,purpose:"DISAGREEMENT_PROBE" as const}));
      }
    }
  }
  return Object.freeze({ independentRoots: BigInt(roots.size), pairs: Object.freeze(pairs) });
}

export function evidenceInformationYieldEstimator(
  distinguishingOutcomes: bigint,
  totalOutcomes: bigint,
  sourceIndependence: Q64
): Q64 {
  if (distinguishingOutcomes < 0n || totalOutcomes <= 0n || distinguishingOutcomes > totalOutcomes) {
    throw new ForgeError("invalid outcome counts");
  }
  q64Unit(sourceIndependence, "source independence");
  return Q64.ratio(distinguishingOutcomes, totalOutcomes).mul(sourceIndependence);
}

export interface SequentialStopResult {
  readonly verdict: "FALSIFIED" | "ENOUGH_FOR_REVIEW" | "CONTINUE";
  readonly authority: AdvisoryAuthority;
  readonly autoPromote: false;
}

export function sequentialEvidenceStopper(
  support: Q64,
  refutation: Q64,
  supportThreshold: Q64,
  refutationThreshold: Q64
): SequentialStopResult {
  q64Unit(support, "support"); q64Unit(refutation, "refutation");
  q64Unit(supportThreshold, "support threshold"); q64Unit(refutationThreshold, "refutation threshold");
  const verdict = refutation.compare(refutationThreshold) >= 0
    ? "FALSIFIED" as const
    : support.compare(supportThreshold) >= 0
      ? "ENOUGH_FOR_REVIEW" as const
      : "CONTINUE" as const;
  return Object.freeze({ verdict, authority: "ADVISORY_ONLY" as const, autoPromote: false as const });
}

export interface Counterexample { readonly id: string; readonly delta: Q64; readonly witness: string; }
export function counterexampleDeltaMinimizer(counterexamples: readonly Counterexample[]): Counterexample {
  if (counterexamples.length === 0) throw new ForgeError("at least one counterexample is required");
  const normalized = counterexamples.map((item) => {
    const id = nonEmpty(item.id, "counterexample id");
    if (item.delta.raw < 0n) throw new ForgeError("counterexample delta must be non-negative");
    return {id,delta:item.delta,witness:nonEmpty(item.witness,"counterexample witness")};
  }).sort((a,b)=>a.delta.compare(b.delta) || a.id.localeCompare(b.id));
  const best = normalized[0];
  if (best === undefined) throw new ForgeError("internal empty counterexample set");
  return Object.freeze(best);
}

