import test from 'node:test';
import assert from 'node:assert/strict';
import { judgeBenefitRegression } from '../dist/benefit_regression.js';

test('marks a candidate BENEFICIAL only with declared improvement and no forbidden regression', () => {
  const result = judgeBenefitRegression(
    [
      { id: 'latency_ms', direction: 'LOWER', critical: true, minImprovement: 10, maxRegression: 0 },
      { id: 'success_bps', direction: 'HIGHER', critical: true, minImprovement: 50, maxRegression: 0 }
    ],
    { latency_ms: 200, success_bps: 9000 },
    { latency_ms: 180, success_bps: 9050 }
  );
  assert.equal(result.status, 'BENEFICIAL');
  assert.deepEqual(result.improvedAxes, ['latency_ms', 'success_bps']);
});

test('rejects a critical regression even when another axis improves', () => {
  const result = judgeBenefitRegression(
    [
      { id: 'latency_ms', direction: 'LOWER', critical: true, minImprovement: 10, maxRegression: 0 },
      { id: 'success_bps', direction: 'HIGHER', critical: true, minImprovement: 50, maxRegression: 0 }
    ],
    { latency_ms: 200, success_bps: 9000 },
    { latency_ms: 150, success_bps: 8999 }
  );
  assert.equal(result.status, 'REJECT');
  assert.deepEqual(result.regressedAxes, ['success_bps']);
});

test('is inconclusive when a required observation is missing', () => {
  const result = judgeBenefitRegression(
    [{ id: 'quality', direction: 'HIGHER', critical: true, minImprovement: 1, maxRegression: 0 }],
    { quality: 10 },
    {}
  );
  assert.equal(result.status, 'INCONCLUSIVE');
  assert.deepEqual(result.missingAxes, ['quality']);
});

test('does not call an unchanged candidate beneficial', () => {
  const result = judgeBenefitRegression(
    [{ id: 'quality', direction: 'HIGHER', critical: true, minImprovement: 1, maxRegression: 0 }],
    { quality: 10 },
    { quality: 10 }
  );
  assert.equal(result.status, 'REJECT');
  assert.deepEqual(result.improvedAxes, []);
});
