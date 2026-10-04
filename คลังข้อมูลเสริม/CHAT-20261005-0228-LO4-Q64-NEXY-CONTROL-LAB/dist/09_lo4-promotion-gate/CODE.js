import { Q64, unit } from "../shared/q64.js";
export function promotionGate(x) {
    const hard = Q64.parse('0.90');
    if (x.determinism.compare(hard) < 0 || x.security.compare(hard) < 0 || x.regression.compare(hard) < 0)
        return { score: Q64.zero(), status: 'REJECT' };
    const score = Q64.weightedMean([unit(x.evidence), unit(x.determinism), unit(x.security), unit(x.regression), unit(x.integration)], [Q64.fromInt(5n), Q64.fromInt(5n), Q64.fromInt(5n), Q64.fromInt(5n), Q64.fromInt(4n)]);
    return { score, status: score.compare(Q64.parse('0.92')) >= 0 ? 'ELIGIBLE_FOR_FORMAL_PROMOTION_REVIEW' : 'HOLD' };
}
