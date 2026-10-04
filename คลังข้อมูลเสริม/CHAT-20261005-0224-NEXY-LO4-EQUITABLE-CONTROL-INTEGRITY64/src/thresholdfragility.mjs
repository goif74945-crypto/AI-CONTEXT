import { cohortRows, rate, rangeGap, validateGapThreshold, requireCount } from './common.mjs';

export function auditThresholdFragility({ cohorts, policy }) {
  const threshold = validateGapThreshold(policy.maxNearBoundaryRateGap, 'maxNearBoundaryRateGap');
  const built = cohortRows(cohorts, policy.minSample, cohort => {
    const near = requireCount(cohort.nearBoundary, `${cohort.id}.nearBoundary`);
    if (near > cohort.total) throw new RangeError(`${cohort.id}.nearBoundary exceeds total`);
    return { cohortId: cohort.id, total: cohort.total, nearBoundary: near, nearBoundaryRate: rate(near, cohort.total, `${cohort.id}.nearBoundaryRate`) };
  });
  if (built.status !== 'OK') return { system: 'THRESHOLD_FRAGILITY64', status: 'FREEZE_FAIRNESS_REVIEW', reason: built.status, cohortId: built.cohortId, rows: [], threshold };
  const { min, max, gap } = rangeGap(built.rows.map(r => r.nearBoundaryRate));
  return {
    system: 'THRESHOLD_FRAGILITY64',
    status: gap.lte(threshold) ? 'PARITY_WITHIN_LIMIT' : 'FREEZE_FAIRNESS_REVIEW',
    reason: gap.lte(threshold) ? 'THRESHOLD_FRAGILITY_GAP_WITHIN_POLICY' : 'THRESHOLD_FRAGILITY_GAP_EXCEEDS_POLICY',
    rows: built.rows, minRate: min, maxRate: max, rateGap: gap, threshold,
  };
}
