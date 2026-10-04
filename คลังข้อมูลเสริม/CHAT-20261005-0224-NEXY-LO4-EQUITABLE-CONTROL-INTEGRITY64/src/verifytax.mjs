import { cohortRows, average, rangeGap, requireCount } from './common.mjs';
import { Q64, ensureQ64 } from './q64.mjs';

export function auditVerificationBurden({ cohorts, policy }) {
  const threshold = ensureQ64(policy.maxAverageBurdenGap);
  if (threshold.lt(Q64.zero())) throw new RangeError('maxAverageBurdenGap must be nonnegative');
  const built = cohortRows(cohorts, policy.minSample, cohort => {
    const requests = requireCount(cohort.total, `${cohort.id}.total`);
    const totalBurden = ensureQ64(cohort.evidenceBurdenTotal);
    if (totalBurden.lt(Q64.zero())) throw new RangeError(`${cohort.id}.evidenceBurdenTotal must be nonnegative`);
    return { cohortId: cohort.id, total: requests, evidenceBurdenTotal: totalBurden, averageBurden: average(totalBurden, requests, `${cohort.id}.averageBurden`) };
  });
  if (built.status !== 'OK') return { system: 'VERIFY_TAX64', status: 'FREEZE_FAIRNESS_REVIEW', reason: built.status, cohortId: built.cohortId, rows: [], threshold };
  const { min, max, gap } = rangeGap(built.rows.map(r => r.averageBurden));
  return {
    system: 'VERIFY_TAX64',
    status: gap.lte(threshold) ? 'PARITY_WITHIN_LIMIT' : 'FREEZE_FAIRNESS_REVIEW',
    reason: gap.lte(threshold) ? 'VERIFICATION_BURDEN_GAP_WITHIN_POLICY' : 'VERIFICATION_BURDEN_GAP_EXCEEDS_POLICY',
    rows: built.rows, minAverageBurden: min, maxAverageBurden: max, burdenGap: gap, threshold,
  };
}
