import { Q64, complement, deterministicSort, requireUniqueIds, unit } from "../shared/q64.js";
export function recoveryScore(p) { return Q64.weightedMean([unit(p.restoreProbability), complement(p.timeCost), complement(p.sideEffectRisk), unit(p.evidence), unit(p.reversibility)], [Q64.fromInt(5n), Q64.fromInt(2n), Q64.fromInt(4n), Q64.fromInt(4n), Q64.fromInt(3n)]); }
export function rankRecovery(plans) { requireUniqueIds(plans, p => p.id); return deterministicSort(plans, recoveryScore, p => p.id); }
