import { Q64, unit } from "../shared/q64.ts";
export type IntentState={confidence:Q64;stability:Q64;direction:-1|0|1};
export type IntentDecision={blended:Q64;oscillation:boolean;acceptCurrent:boolean};
export function filterIntent(previous:IntentState,current:IntentState,hysteresis:Q64):IntentDecision{const oscillation=previous.direction!==0&&current.direction!==0&&previous.direction!==current.direction;const priorWeight=oscillation?Q64.fromInt(3n):Q64.one();const currentWeight=Q64.fromInt(4n);const blended=Q64.weightedMean([unit(previous.confidence.mul(previous.stability)),unit(current.confidence.mul(current.stability))],[priorWeight,currentWeight]);return{blended,oscillation,acceptCurrent:!oscillation||blended.compare(hysteresis)>=0};}
