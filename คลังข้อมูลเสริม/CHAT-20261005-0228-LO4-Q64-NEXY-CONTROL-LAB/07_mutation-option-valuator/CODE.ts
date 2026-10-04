import { Q64, complement, unit } from "../shared/q64.ts";
export type MutationOption={id:string;utility:Q64;reversibility:Q64;blastRadius:Q64;rollbackCost:Q64;evidence:Q64};
export function optionValue(o:MutationOption):Q64{return Q64.weightedMean([unit(o.utility),unit(o.reversibility),complement(o.blastRadius),complement(o.rollbackCost),unit(o.evidence)],[Q64.fromInt(4n),Q64.fromInt(4n),Q64.fromInt(5n),Q64.fromInt(3n),Q64.fromInt(5n)]);}
