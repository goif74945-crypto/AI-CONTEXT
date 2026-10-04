import { cohortRows, rate, rangeGap, validateGapThreshold, requireCount } from './common.mjs';

export function auditFreezeBurden({ cohorts, policy }) {
  const threshold = validateGapThreshold(policy.maxFreezeRateGap, 'maxFreezeRateGap');
  const built = cohortRows(cohorts, policy.minSample, cohort => {
    const freezes = requireCount(cohort.freezes, `${cohort.id}.freezes`);
    if (freezes > cohort.total) throw new RangeError(`${cohort.id}.freezes exceeds total`);
    return { cohortId: cohort.id, total: cohort.total, freezes, freezeRate: rate(freezes, cohort.total, `${cohort.id}.freezeRate`) };
  });
  if (built.status !== 'OK') return freeze('FREEZE_EQ64', built.status, built.cohortId, threshold);
  const { min, max, gap } = rangeGap(built.rows.map(r => r.freezeRate));
  return {
    system: 'FREEZE_EQ64',
    status: gap.lte(threshold) ? 'PARITY_WITHIN_LIMIT' : 'FREEZE_FAIRNESS_REVIEW',
    reason: gap.lte(threshold) ? 'FREEZE_RATE_GAP_WITHIN_POLICY' : 'FREEZE_RATE_GAP_EXCEEDS_POLICY',
    rows: built.rows, minRate: min, maxRate: max, rateGap: gap, threshold,
  };
}

function freeze(system, reason, cohortId, threshold) {
  return { system, status: 'FREEZE_FAIRNESS_REVIEW', reason, cohortId, rows: [], threshold };
}
