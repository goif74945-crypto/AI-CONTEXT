import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function routeScore(c, w) {
    return Q64.weightedMean([unit(c.quality), complement(c.latency), complement(c.cost), unit(c.safety), unit(c.stability)], [w.quality, w.latency, w.cost, w.safety, w.stability]);
}
export function chooseModel(candidates, w, minSafety) {
    requireUniqueIds(candidates, c => c.id);
    const eligible = candidates.filter(c => c.safety.compare(minSafety) >= 0);
    if (!eligible.length)
        throw new Error('NO_SAFE_MODEL');
    return deterministicSort(eligible, c => routeScore(c, w), c => c.id)[0];
}
