import { cohortRows, rate, rangeGap, validateGapThreshold, requireCount } from './common.mjs';

export function auditAvoidableFreeze({ cohorts, policy }) {
  const threshold = validateGapThreshold(policy.maxAvoidableFreezeRateGap, 'maxAvoidableFreezeRateGap');
  const built = cohortRows(cohorts, policy.minSample, cohort => {
    const freezes = requireCount(cohort.freezes, `${cohort.id}.freezes`);
    const avoidable = requireCount(cohort.avoidableFreezes, `${cohort.id}.avoidableFreezes`);
    if (freezes > cohort.total) throw new RangeError(`${cohort.id}.freezes exceeds total`);
    if (avoidable > freezes) throw new RangeError(`${cohort.id}.avoidableFreezes exceeds freezes`);
    return {
      cohortId: cohort.id,
      total: cohort.total,
      freezes,
      avoidableFreezes: avoidable,
      avoidableFreezeRate: rate(avoidable, cohort.total, `${cohort.id}.avoidableFreezeRate`),
    };
  });
  if (built.status !== 'OK') return { system: 'UNNECESSARY_FREEZE64', status: 'FREEZE_FAIRNESS_REVIEW', reason: built.status, cohortId: built.cohortId, rows: [], threshold };
  const { min, max, gap } = rangeGap(built.rows.map(r => r.avoidableFreezeRate));
  return {
    system: 'UNNECESSARY_FREEZE64',
    status: gap.lte(threshold) ? 'PARITY_WITHIN_LIMIT' : 'FREEZE_FAIRNESS_REVIEW',
    reason: gap.lte(threshold) ? 'AVOIDABLE_FREEZE_GAP_WITHIN_POLICY' : 'AVOIDABLE_FREEZE_GAP_EXCEEDS_POLICY',
    rows: built.rows, minRate: min, maxRate: max, rateGap: gap, threshold,
  };
}
