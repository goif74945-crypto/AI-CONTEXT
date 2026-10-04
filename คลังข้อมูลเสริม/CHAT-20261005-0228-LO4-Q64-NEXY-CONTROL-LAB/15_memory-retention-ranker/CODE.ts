import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type MemoryCandidate={id:string;futureUtility:Q64;authority:Q64;uniqueness:Q64;freshness:Q64;privacyCost:Q64};
export function retentionScore(m:MemoryCandidate):Q64{return Q64.weightedMean([unit(m.futureUtility),unit(m.authority),unit(m.uniqueness),unit(m.freshness),complement(m.privacyCost)],[Q64.fromInt(5n),Q64.fromInt(5n),Q64.fromInt(4n),Q64.fromInt(2n),Q64.fromInt(5n)]);}
export function rankMemory(m:readonly MemoryCandidate[]):MemoryCandidate[]{requireUniqueIds(m,x=>x.id);return deterministicSort(m,retentionScore,x=>x.id)}
