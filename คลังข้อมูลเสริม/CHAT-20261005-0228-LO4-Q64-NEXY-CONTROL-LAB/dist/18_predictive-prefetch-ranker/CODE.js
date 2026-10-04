import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function prefetchScore(c) { return Q64.weightedMean([unit(c.probability), unit(c.utility), complement(c.sizeCost), unit(c.freshness), complement(c.wasteRisk)], [Q64.fromInt(5n), Q64.fromInt(4n), Q64.fromInt(2n), Q64.fromInt(3n), Q64.fromInt(4n)]); }
export function rankPrefetch(c) { requireUniqueIds(c, x => x.id); return deterministicSort(c, prefetchScore, x => x.id); }
