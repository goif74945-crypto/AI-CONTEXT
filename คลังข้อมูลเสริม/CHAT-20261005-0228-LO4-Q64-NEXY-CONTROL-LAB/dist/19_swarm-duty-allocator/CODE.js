import { Q64, ZERO, complement, requireUniqueIds, unit } from "../shared/q64.js";
export function allocateDuty(agents) {
    if (!agents.length)
        return [];
    requireUniqueIds(agents, a => a.id);
    const as = [...agents].sort((a, b) => a.id.localeCompare(b.id));
    const scores = as.map(a => Q64.weightedMean([unit(a.capacity), unit(a.fitness), unit(a.trust), complement(a.load), unit(a.reserve)], [Q64.fromInt(4n), Q64.fromInt(5n), Q64.fromInt(5n), Q64.fromInt(3n), Q64.fromInt(2n)]));
    const total = Q64.sum(scores);
    if (total.isZero())
        return as.map(a => ({ id: a.id, share: ZERO, rawScore: ZERO }));
    let assigned = ZERO;
    return as.map((a, i) => { const share = i === as.length - 1 ? Q64.one().sub(assigned) : scores[i].div(total); assigned = assigned.add(share); return { id: a.id, share, rawScore: scores[i] }; });
}
