import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function toolScore(t) { return Q64.weightedMean([unit(t.expectedUtility), unit(t.confidence), complement(t.latencyCost), complement(t.moneyCost), complement(t.mutationRisk)], [Q64.fromInt(5n), Q64.fromInt(4n), Q64.fromInt(2n), Q64.fromInt(2n), Q64.fromInt(5n)]); }
export function rankTools(ts) { requireUniqueIds(ts, t => t.id); return deterministicSort(ts, toolScore, t => t.id); }
export function requireTool(t, min) { const s = toolScore(t); if (s.compare(min) < 0)
    throw new Error('TOOL_CALL_REJECTED'); return s; }
