import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function salience(c) { return Q64.weightedMean([unit(c.relevance), unit(c.authority), unit(c.freshness), unit(c.userPriority), complement(c.contaminationRisk)], [Q64.fromInt(4n), Q64.fromInt(4n), Q64.fromInt(2n), Q64.fromInt(3n), Q64.fromInt(5n)]); }
export function rankContext(chunks) { requireUniqueIds(chunks, c => c.id); return deterministicSort(chunks, salience, c => c.id); }
