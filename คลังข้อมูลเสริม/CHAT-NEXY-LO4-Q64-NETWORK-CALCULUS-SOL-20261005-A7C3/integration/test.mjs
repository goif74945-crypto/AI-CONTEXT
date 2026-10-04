import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { certifyChain } from '../dist/04_CHAIN_64/src.js';
import { synthesizeShaper } from '../dist/05_SHAPER_64/src.js';

test('shaper repairs an initially non-admissible multi-stage flow', () => {
  const stages = [
    {id:'gateway', rateQ:qInt(8n), latencyQ:qInt(1n)},
    {id:'core', rateQ:qInt(5n), latencyQ:qInt(2n)},
    {id:'judge', rateQ:qInt(6n), latencyQ:qInt(1n)}
  ];
  const offered = { burstQ:qInt(30n), rateQ:qInt(7n) };
  const before = certifyChain(offered, stages, {maxDelayQ:qInt(8n), maxBacklogQ:qInt(24n)});
  assert.notEqual(before.verdict, 'PASS');

  const shaped = synthesizeShaper(offered, before.composedService, {maxDelayQ:qInt(8n), maxBacklogQ:qInt(24n)});
  assert.equal(shaped.verdict, 'SHAPED');

  const after = certifyChain(shaped.shaped, stages, {maxDelayQ:qInt(8n), maxBacklogQ:qInt(24n)});
  assert.equal(after.verdict, 'PASS');
  assert.equal(after.delayBoundQ <= qInt(8n), true);
  assert.equal(after.backlogBoundQ <= qInt(24n), true);
});
