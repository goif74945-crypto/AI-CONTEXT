import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type ToolCall={id:string;expectedUtility:Q64;confidence:Q64;latencyCost:Q64;moneyCost:Q64;mutationRisk:Q64};
export function toolScore(t:ToolCall):Q64{return Q64.weightedMean([unit(t.expectedUtility),unit(t.confidence),complement(t.latencyCost),complement(t.moneyCost),complement(t.mutationRisk)],[Q64.fromInt(5n),Q64.fromInt(4n),Q64.fromInt(2n),Q64.fromInt(2n),Q64.fromInt(5n)]);}
export function rankTools(ts:readonly ToolCall[]):ToolCall[]{requireUniqueIds(ts,t=>t.id);return deterministicSort(ts,toolScore,t=>t.id)}
export function requireTool(t:ToolCall,min:Q64):Q64{const s=toolScore(t);if(s.compare(min)<0)throw new Error('TOOL_CALL_REJECTED');return s}
