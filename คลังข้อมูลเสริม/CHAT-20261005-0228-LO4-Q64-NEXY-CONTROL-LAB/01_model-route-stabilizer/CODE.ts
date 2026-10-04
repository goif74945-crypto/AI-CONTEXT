import { Q64, ONE, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type ModelCandidate = { id:string; quality:Q64; latency:Q64; cost:Q64; safety:Q64; stability:Q64 };
export type RouteWeights = { quality:Q64; latency:Q64; cost:Q64; safety:Q64; stability:Q64 };
export function routeScore(c:ModelCandidate,w:RouteWeights):Q64 {
  return Q64.weightedMean([unit(c.quality),complement(c.latency),complement(c.cost),unit(c.safety),unit(c.stability)], [w.quality,w.latency,w.cost,w.safety,w.stability]);
}
export function chooseModel(candidates:readonly ModelCandidate[],w:RouteWeights,minSafety:Q64):ModelCandidate {
  requireUniqueIds(candidates,c=>c.id);
  const eligible=candidates.filter(c=>c.safety.compare(minSafety)>=0);
  if(!eligible.length) throw new Error('NO_SAFE_MODEL');
  return deterministicSort(eligible,c=>routeScore(c,w),c=>c.id)[0];
}
