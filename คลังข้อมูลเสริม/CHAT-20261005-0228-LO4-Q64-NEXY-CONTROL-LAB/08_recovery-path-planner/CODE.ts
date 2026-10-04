import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.ts";
export type RecoveryPlan={id:string;restoreProbability:Q64;timeCost:Q64;sideEffectRisk:Q64;evidence:Q64;reversibility:Q64};
export function recoveryScore(p:RecoveryPlan):Q64{return Q64.weightedMean([unit(p.restoreProbability),complement(p.timeCost),complement(p.sideEffectRisk),unit(p.evidence),unit(p.reversibility)],[Q64.fromInt(5n),Q64.fromInt(2n),Q64.fromInt(4n),Q64.fromInt(4n),Q64.fromInt(3n)]);}
export function rankRecovery(plans:readonly RecoveryPlan[]):RecoveryPlan[]{requireUniqueIds(plans,p=>p.id);return deterministicSort(plans,recoveryScore,p=>p.id);}
