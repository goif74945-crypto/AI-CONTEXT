import { Q64, unit } from "../shared/q64.ts";
export type Incident={impact:Q64;reach:Q64;exploitability:Q64;irreversibility:Q64;spread:Q64};
export type Severity={score:Q64;level:'S1'|'S2'|'S3'|'S4'};
export function severity(i:Incident):Severity{const score=Q64.weightedMean([unit(i.impact),unit(i.reach),unit(i.exploitability),unit(i.irreversibility),unit(i.spread)],[Q64.fromInt(5n),Q64.fromInt(4n),Q64.fromInt(4n),Q64.fromInt(5n),Q64.fromInt(5n)]);return{score,level:score.compare(Q64.parse('0.85'))>=0?'S4':score.compare(Q64.parse('0.65'))>=0?'S3':score.compare(Q64.parse('0.35'))>=0?'S2':'S1'}}
