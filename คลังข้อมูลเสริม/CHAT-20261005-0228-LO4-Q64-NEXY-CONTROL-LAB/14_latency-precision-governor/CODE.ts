import { Q64, complement, unit } from "../shared/q64.ts";
export type PrecisionDecision={score:Q64;tier:'FAST'|'BALANCED'|'DEEP'};
export function choosePrecision(importance:Q64,urgency:Q64,latencyPressure:Q64,uncertainty:Q64):PrecisionDecision{const score=Q64.weightedMean([unit(importance),complement(urgency),complement(latencyPressure),unit(uncertainty)],[Q64.fromInt(4n),Q64.fromInt(2n),Q64.fromInt(3n),Q64.fromInt(4n)]);return{score,tier:score.compare(Q64.parse('0.72'))>=0?'DEEP':score.compare(Q64.parse('0.42'))>=0?'BALANCED':'FAST'};}
