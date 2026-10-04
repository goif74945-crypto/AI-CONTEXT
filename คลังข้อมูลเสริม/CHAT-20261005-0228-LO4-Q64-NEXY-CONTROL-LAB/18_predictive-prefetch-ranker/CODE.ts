import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type PrefetchCandidate={id:string;probability:Q64;utility:Q64;sizeCost:Q64;freshness:Q64;wasteRisk:Q64};
export function prefetchScore(c:PrefetchCandidate):Q64{return Q64.weightedMean([unit(c.probability),unit(c.utility),complement(c.sizeCost),unit(c.freshness),complement(c.wasteRisk)],[Q64.fromInt(5n),Q64.fromInt(4n),Q64.fromInt(2n),Q64.fromInt(3n),Q64.fromInt(4n)]);}
export function rankPrefetch(c:readonly PrefetchCandidate[]):PrefetchCandidate[]{requireUniqueIds(c,x=>x.id);return deterministicSort(c,prefetchScore,x=>x.id)}
