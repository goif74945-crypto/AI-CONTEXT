import test from 'node:test';
import assert from 'node:assert/strict';
import {
  Q64,
  auditFreezeBurden,
  auditVerificationBurden,
  auditAvoidableFreeze,
  auditRecoveryEquity,
  auditThresholdFragility,
} from '../src/index.mjs';

const q = Q64.parse;

function baseCohorts() {
  return [
    {
      id: 'cohort-A', total: 100n, freezes: 10n, avoidableFreezes: 2n,
      evidenceBurdenTotal: q('100'), recoveryEligible: 10n, recovered: 8n,
      recoveryDurationTotal: q('16'), nearBoundary: 10n,
    },
    {
      id: 'cohort-B', total: 100n, freezes: 12n, avoidableFreezes: 3n,
      evidenceBurdenTotal: q('120'), recoveryEligible: 10n, recovered: 9n,
      recoveryDurationTotal: q('27'), nearBoundary: 15n,
    },
  ];
}

test('FREEZE_EQ64 passes a small explicit freeze-rate gap', () => {
  const out = auditFreezeBurden({ cohorts: baseCohorts(), policy: { minSample: 50n, maxFreezeRateGap: q('0.03') } });
  assert.equal(out.status, 'PARITY_WITHIN_LIMIT');
  assert(out.rateGap.lte(q('0.03')));
});

test('FREEZE_EQ64 freezes a large freeze-rate gap', () => {
  const c = baseCohorts();
  c[1].freezes = 35n;
  const out = auditFreezeBurden({ cohorts: c, policy: { minSample: 50n, maxFreezeRateGap: q('0.10') } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
  assert.equal(out.reason, 'FREEZE_RATE_GAP_EXCEEDS_POLICY');
});

test('FREEZE_EQ64 freezes insufficient sample instead of smoothing it away', () => {
  const c = baseCohorts();
  c[0].total = 5n;
  c[0].freezes = 1n;
  const out = auditFreezeBurden({ cohorts: c, policy: { minSample: 50n, maxFreezeRateGap: q('0.10') } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
  assert.equal(out.reason, 'INSUFFICIENT_SAMPLE');
});

test('VERIFY_TAX64 passes bounded average verification burden gap', () => {
  const out = auditVerificationBurden({ cohorts: baseCohorts(), policy: { minSample: 50n, maxAverageBurdenGap: q('0.25') } });
  assert.equal(out.status, 'PARITY_WITHIN_LIMIT');
  assert(out.burdenGap.lte(q('0.25')));
});

test('VERIFY_TAX64 freezes excessive verification burden disparity', () => {
  const c = baseCohorts();
  c[1].evidenceBurdenTotal = q('300');
  const out = auditVerificationBurden({ cohorts: c, policy: { minSample: 50n, maxAverageBurdenGap: q('0.50') } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
});

test('VERIFY_TAX64 rejects negative burden', () => {
  const c = baseCohorts();
  c[0].evidenceBurdenTotal = q('-1');
  assert.throws(() => auditVerificationBurden({ cohorts: c, policy: { minSample: 50n, maxAverageBurdenGap: q('0.50') } }), RangeError);
});

test('UNNECESSARY_FREEZE64 passes bounded avoidable-freeze gap', () => {
  const out = auditAvoidableFreeze({ cohorts: baseCohorts(), policy: { minSample: 50n, maxAvoidableFreezeRateGap: q('0.02') } });
  assert.equal(out.status, 'PARITY_WITHIN_LIMIT');
});

test('UNNECESSARY_FREEZE64 freezes avoidable-freeze disparity', () => {
  const c = baseCohorts();
  c[1].freezes = 40n;
  c[1].avoidableFreezes = 20n;
  const out = auditAvoidableFreeze({ cohorts: c, policy: { minSample: 50n, maxAvoidableFreezeRateGap: q('0.05') } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
});

test('UNNECESSARY_FREEZE64 rejects impossible avoidable count', () => {
  const c = baseCohorts();
  c[0].avoidableFreezes = 11n;
  assert.throws(() => auditAvoidableFreeze({ cohorts: c, policy: { minSample: 50n, maxAvoidableFreezeRateGap: q('0.10') } }), RangeError);
});

test('RECOVERY_EQ64 passes bounded recovery-rate and time gaps', () => {
  const out = auditRecoveryEquity({ cohorts: baseCohorts(), policy: {
    minSample: 50n, maxRecoveryRateGap: q('0.15'), maxAverageRecoveryTimeGap: q('1.1')
  } });
  assert.equal(out.status, 'PARITY_WITHIN_LIMIT');
});

test('RECOVERY_EQ64 freezes rate disparity', () => {
  const c = baseCohorts();
  c[1].recovered = 2n;
  c[1].recoveryDurationTotal = q('4');
  const out = auditRecoveryEquity({ cohorts: c, policy: {
    minSample: 50n, maxRecoveryRateGap: q('0.20'), maxAverageRecoveryTimeGap: q('5')
  } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
});

test('RECOVERY_EQ64 freezes if recovery duration is unobservable', () => {
  const c = baseCohorts();
  c[1].recovered = 0n;
  c[1].recoveryDurationTotal = q('0');
  const out = auditRecoveryEquity({ cohorts: c, policy: {
    minSample: 50n, maxRecoveryRateGap: q('1'), maxAverageRecoveryTimeGap: q('5')
  } });
  assert.equal(out.reason, 'NO_RECOVERY_DURATION_OBSERVATION');
});

test('THRESHOLD_FRAGILITY64 passes bounded near-boundary gap', () => {
  const out = auditThresholdFragility({ cohorts: baseCohorts(), policy: { minSample: 50n, maxNearBoundaryRateGap: q('0.10') } });
  assert.equal(out.status, 'PARITY_WITHIN_LIMIT');
});

test('THRESHOLD_FRAGILITY64 freezes asymmetric threshold fragility', () => {
  const c = baseCohorts();
  c[1].nearBoundary = 50n;
  const out = auditThresholdFragility({ cohorts: c, policy: { minSample: 50n, maxNearBoundaryRateGap: q('0.10') } });
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
});

test('all auditors reject duplicate cohort IDs', () => {
  const c = baseCohorts();
  c[1].id = c[0].id;
  assert.throws(() => auditFreezeBurden({ cohorts: c, policy: { minSample: 50n, maxFreezeRateGap: q('0.10') } }), TypeError);
});
