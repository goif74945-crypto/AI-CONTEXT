import { cohortRows, rate, rangeGap, validateGapThreshold, requireCount, average } from './common.mjs';
import { Q64, ensureQ64 } from './q64.mjs';

export function auditRecoveryEquity({ cohorts, policy }) {
  const maxRateGap = validateGapThreshold(policy.maxRecoveryRateGap, 'maxRecoveryRateGap');
  const maxTimeGap = ensureQ64(policy.maxAverageRecoveryTimeGap);
  if (maxTimeGap.lt(Q64.zero())) throw new RangeError('maxAverageRecoveryTimeGap must be nonnegative');
  const built = cohortRows(cohorts, policy.minSample, cohort => {
    const eligible = requireCount(cohort.recoveryEligible, `${cohort.id}.recoveryEligible`);
    const recovered = requireCount(cohort.recovered, `${cohort.id}.recovered`);
    if (eligible > cohort.total) throw new RangeError(`${cohort.id}.recoveryEligible exceeds total`);
    if (recovered > eligible) throw new RangeError(`${cohort.id}.recovered exceeds recoveryEligible`);
    const duration = ensureQ64(cohort.recoveryDurationTotal);
    if (duration.lt(Q64.zero())) throw new RangeError(`${cohort.id}.recoveryDurationTotal must be nonnegative`);
    if (eligible === 0n) throw new RangeError(`${cohort.id}.recoveryEligible must be > 0 for recovery audit`);
    const recoveryRate = rate(recovered, eligible, `${cohort.id}.recoveryRate`);
    const averageRecoveryTime = recovered === 0n ? null : average(duration, recovered, `${cohort.id}.averageRecoveryTime`);
    return { cohortId: cohort.id, total: cohort.total, eligible, recovered, recoveryRate, averageRecoveryTime };
  });
  if (built.status !== 'OK') return { system: 'RECOVERY_EQ64', status: 'FREEZE_FAIRNESS_REVIEW', reason: built.status, cohortId: built.cohortId, rows: [], maxRateGap, maxTimeGap };
  if (built.rows.some(r => r.averageRecoveryTime === null)) {
    return { system: 'RECOVERY_EQ64', status: 'FREEZE_FAIRNESS_REVIEW', reason: 'NO_RECOVERY_DURATION_OBSERVATION', rows: built.rows, maxRateGap, maxTimeGap };
  }
  const rateStats = rangeGap(built.rows.map(r => r.recoveryRate));
  const timeStats = rangeGap(built.rows.map(r => r.averageRecoveryTime));
  const ok = rateStats.gap.lte(maxRateGap) && timeStats.gap.lte(maxTimeGap);
  return {
    system: 'RECOVERY_EQ64',
    status: ok ? 'PARITY_WITHIN_LIMIT' : 'FREEZE_FAIRNESS_REVIEW',
    reason: ok ? 'RECOVERY_GAPS_WITHIN_POLICY' : 'RECOVERY_GAP_EXCEEDS_POLICY',
    rows: built.rows,
    recoveryRateGap: rateStats.gap,
    averageRecoveryTimeGap: timeStats.gap,
    maxRateGap,
    maxTimeGap,
  };
}
