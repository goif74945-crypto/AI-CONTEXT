import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type ContextChunk={id:string; relevance:Q64; authority:Q64; freshness:Q64; userPriority:Q64; contaminationRisk:Q64};
export function salience(c:ContextChunk):Q64 { return Q64.weightedMean([unit(c.relevance),unit(c.authority),unit(c.freshness),unit(c.userPriority),complement(c.contaminationRisk)],[Q64.fromInt(4n),Q64.fromInt(4n),Q64.fromInt(2n),Q64.fromInt(3n),Q64.fromInt(5n)]); }
export function rankContext(chunks:readonly ContextChunk[]):ContextChunk[]{ requireUniqueIds(chunks,c=>c.id); return deterministicSort(chunks,salience,c=>c.id); }
