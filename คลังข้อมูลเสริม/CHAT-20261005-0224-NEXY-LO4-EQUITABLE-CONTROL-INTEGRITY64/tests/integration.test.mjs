import test from 'node:test';
import assert from 'node:assert/strict';
import { Q64, auditEquitableControlPack } from '../src/index.mjs';
const q = Q64.parse;

function input() {
  return {
    cohorts: [
      { id: 'A', total: 100n, freezes: 10n, avoidableFreezes: 2n, evidenceBurdenTotal: q('100'), recoveryEligible: 10n, recovered: 8n, recoveryDurationTotal: q('16'), nearBoundary: 10n },
      { id: 'B', total: 100n, freezes: 12n, avoidableFreezes: 3n, evidenceBurdenTotal: q('120'), recoveryEligible: 10n, recovered: 9n, recoveryDurationTotal: q('27'), nearBoundary: 15n },
    ],
    policies: {
      freeze: { minSample: 50n, maxFreezeRateGap: q('0.03') },
      verification: { minSample: 50n, maxAverageBurdenGap: q('0.25') },
      avoidable: { minSample: 50n, maxAvoidableFreezeRateGap: q('0.02') },
      recovery: { minSample: 50n, maxRecoveryRateGap: q('0.15'), maxAverageRecoveryTimeGap: q('1.1') },
      threshold: { minSample: 50n, maxNearBoundaryRateGap: q('0.10') },
    }
  };
}

test('equitable control pack passes only when all five audits pass', () => {
  const out = auditEquitableControlPack(input());
  assert.equal(out.status, 'READY_FOR_HUMAN_REVIEW');
  assert.deepEqual(out.frozenSystems, []);
  assert.equal(out.results.length, 5);
  assert.match(out.authorityNotice, /advisory Lo4 evidence/i);
});

test('equitable control pack freezes when one cohort suffers excessive freeze burden', () => {
  const x = input();
  x.cohorts[1].freezes = 40n;
  x.cohorts[1].avoidableFreezes = 3n;
  const out = auditEquitableControlPack(x);
  assert.equal(out.status, 'FREEZE_FAIRNESS_REVIEW');
  assert(out.frozenSystems.includes('FREEZE_EQ64'));
});

test('pipeline does not infer cohort labels or sensitive attributes', () => {
  const x = input();
  x.cohorts[0].id = 'opaque-001';
  x.cohorts[1].id = 'opaque-002';
  const out = auditEquitableControlPack(x);
  assert.equal(out.status, 'READY_FOR_HUMAN_REVIEW');
  assert.equal(out.results[0].rows[0].cohortId, 'opaque-001');
});
