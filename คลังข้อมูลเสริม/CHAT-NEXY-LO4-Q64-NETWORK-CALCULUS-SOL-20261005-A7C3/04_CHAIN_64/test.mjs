import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { composeChain, certifyChain } from '../dist/04_CHAIN_64/src.js';

test('composes rate-latency chain as min-rate plus latency sum', () => {
  const c = composeChain([
    { id:'ingress', rateQ:qInt(8n), latencyQ:qInt(1n) },
    { id:'judge', rateQ:qInt(5n), latencyQ:qInt(2n) },
    { id:'egress', rateQ:qInt(7n), latencyQ:qInt(1n) }
  ]);
  assert.equal(c.service.rateQ, qInt(5n));
  assert.equal(c.service.latencyQ, qInt(4n));
  const r = certifyChain({ burstQ:qInt(10n), rateQ:qInt(2n) }, c.stages, { maxDelayQ:qInt(6n), maxBacklogQ:qInt(18n) });
  assert.equal(r.verdict, 'PASS');
});

test('freezes empty or invalid chain', () => {
  assert.equal(composeChain([]).verdict, 'FREEZE');
  assert.equal(composeChain([{id:'x', rateQ:0n, latencyQ:0n}]).verdict, 'FREEZE');
});
