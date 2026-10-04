import { Q64, complement, unit } from "../shared/q64.js";
export function optionValue(o) { return Q64.weightedMean([unit(o.utility), unit(o.reversibility), complement(o.blastRadius), complement(o.rollbackCost), unit(o.evidence)], [Q64.fromInt(4n), Q64.fromInt(4n), Q64.fromInt(5n), Q64.fromInt(3n), Q64.fromInt(5n)]); }
