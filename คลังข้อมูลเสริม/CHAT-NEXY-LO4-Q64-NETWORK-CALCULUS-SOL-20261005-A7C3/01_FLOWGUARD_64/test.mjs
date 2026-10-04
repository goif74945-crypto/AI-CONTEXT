import test from 'node:test';
import assert from 'node:assert/strict';
import { Q64_ONE, qInt } from '../dist/shared/q64.js';
import { certifyFlow } from '../dist/01_FLOWGUARD_64/src.js';

test('admits stable token-bucket flow', () => {
  const r = certifyFlow({ burstQ: qInt(10n), rateQ: qInt(2n) }, { rateQ: qInt(5n), latencyQ: qInt(3n) });
  assert.equal(r.verdict, 'ADMIT');
  assert.equal(r.backlogBoundQ, qInt(16n));
  assert.equal(r.delayBoundQ, qInt(5n));
  assert.equal(typeof r.fingerprint, 'string');
  assert.equal(r.fingerprint.length, 64);
});

test('rejects unstable rate and freezes malformed input', () => {
  assert.equal(certifyFlow({ burstQ: qInt(1n), rateQ: qInt(6n) }, { rateQ: qInt(5n), latencyQ: 0n }).verdict, 'REJECT');
  assert.equal(certifyFlow({ burstQ: -Q64_ONE, rateQ: qInt(1n) }, { rateQ: qInt(5n), latencyQ: 0n }).verdict, 'FREEZE');
});
