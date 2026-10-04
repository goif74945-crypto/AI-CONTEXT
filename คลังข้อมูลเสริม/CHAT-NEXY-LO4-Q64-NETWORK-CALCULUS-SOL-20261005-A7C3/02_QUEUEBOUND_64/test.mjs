import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { certifyBacklog } from '../dist/02_QUEUEBOUND_64/src.js';

test('computes worst-case backlog b+rT', () => {
  const r = certifyBacklog({ burstQ:qInt(8n), rateQ:qInt(2n) }, { rateQ:qInt(4n), latencyQ:qInt(3n) }, qInt(14n));
  assert.equal(r.backlogBoundQ, qInt(14n));
  assert.equal(r.verdict, 'PASS');
});

test('fails buffer cap and unstable service', () => {
  assert.equal(certifyBacklog({ burstQ:qInt(8n), rateQ:qInt(2n) }, { rateQ:qInt(4n), latencyQ:qInt(3n) }, qInt(13n)).verdict, 'FAIL');
  assert.equal(certifyBacklog({ burstQ:qInt(1n), rateQ:qInt(5n) }, { rateQ:qInt(4n), latencyQ:qInt(1n) }).verdict, 'FREEZE');
});
