import test from 'node:test';
import assert from 'node:assert/strict';
import { summarizeProgress } from '../dist/progress_truth.js';

test('allows COMPLETE only when every obligation passes', () => {
  const result = summarizeProgress([
    { id: 'design', status: 'PASS' },
    { id: 'code', status: 'PASS' },
    { id: 'tests', status: 'PASS' }
  ]);
  assert.equal(result.aggregate, 'COMPLETE');
  assert.equal(result.completeClaimAllowed, true);
  assert.equal(result.passRatioBps, 10000);
});

test('unknown work prevents a completion claim', () => {
  const result = summarizeProgress([
    { id: 'design', status: 'PASS' },
    { id: 'runtime', status: 'UNKNOWN' }
  ]);
  assert.equal(result.aggregate, 'NOT_VERIFIED');
  assert.equal(result.completeClaimAllowed, false);
  assert.equal(result.passRatioBps, 5000);
});

test('blocked outranks pending', () => {
  const result = summarizeProgress([
    { id: 'a', status: 'PENDING' },
    { id: 'b', status: 'BLOCKED' }
  ]);
  assert.equal(result.aggregate, 'BLOCKED');
});

test('empty obligation set is not verified', () => {
  const result = summarizeProgress([]);
  assert.equal(result.aggregate, 'NOT_VERIFIED');
  assert.equal(result.passRatioBps, null);
});
