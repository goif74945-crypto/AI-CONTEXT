import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function retentionScore(m) { return Q64.weightedMean([unit(m.futureUtility), unit(m.authority), unit(m.uniqueness), unit(m.freshness), complement(m.privacyCost)], [Q64.fromInt(5n), Q64.fromInt(5n), Q64.fromInt(4n), Q64.fromInt(2n), Q64.fromInt(5n)]); }
export function rankMemory(m) { requireUniqueIds(m, x => x.id); return deterministicSort(m, retentionScore, x => x.id); }
