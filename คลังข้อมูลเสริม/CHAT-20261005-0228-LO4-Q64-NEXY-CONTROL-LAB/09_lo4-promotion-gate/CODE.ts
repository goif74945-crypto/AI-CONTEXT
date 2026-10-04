import { Q64, unit } from "../shared/q64.ts";
export type PromotionEvidence={evidence:Q64;determinism:Q64;security:Q64;regression:Q64;integration:Q64};
export type PromotionDecision={score:Q64;status:'REJECT'|'HOLD'|'ELIGIBLE_FOR_FORMAL_PROMOTION_REVIEW'};
export function promotionGate(x:PromotionEvidence):PromotionDecision{
 const hard=Q64.parse('0.90'); if(x.determinism.compare(hard)<0||x.security.compare(hard)<0||x.regression.compare(hard)<0)return {score:Q64.zero(),status:'REJECT'};
 const score=Q64.weightedMean([unit(x.evidence),unit(x.determinism),unit(x.security),unit(x.regression),unit(x.integration)],[Q64.fromInt(5n),Q64.fromInt(5n),Q64.fromInt(5n),Q64.fromInt(5n),Q64.fromInt(4n)]);
 return {score,status:score.compare(Q64.parse('0.92'))>=0?'ELIGIBLE_FOR_FORMAL_PROMOTION_REVIEW':'HOLD'};
}
