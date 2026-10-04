import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { certifyDeadline } from '../dist/03_DEADLINE_64/src.js';

test('computes conservative delay T+ceil(b/R)', () => {
  const r = certifyDeadline({ burstQ:qInt(10n), rateQ:qInt(2n) }, { rateQ:qInt(5n), latencyQ:qInt(3n) }, qInt(5n));
  assert.equal(r.delayBoundQ, qInt(5n));
  assert.equal(r.verdict, 'PASS');
});

test('fails tight deadline and freezes zero service', () => {
  assert.equal(certifyDeadline({ burstQ:qInt(10n), rateQ:qInt(2n) }, { rateQ:qInt(5n), latencyQ:qInt(3n) }, qInt(4n)).verdict, 'FAIL');
  assert.equal(certifyDeadline({ burstQ:qInt(1n), rateQ:0n }, { rateQ:0n, latencyQ:0n }).verdict, 'FREEZE');
});
