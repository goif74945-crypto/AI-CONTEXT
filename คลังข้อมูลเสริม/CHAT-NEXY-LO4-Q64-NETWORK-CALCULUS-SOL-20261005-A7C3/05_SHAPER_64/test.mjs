import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { synthesizeShaper } from '../dist/05_SHAPER_64/src.js';

test('shapes rate and burst to meet backlog and delay contract', () => {
  const r = synthesizeShaper(
    { burstQ:qInt(20n), rateQ:qInt(9n) },
    { rateQ:qInt(5n), latencyQ:qInt(2n) },
    { maxBacklogQ:qInt(16n), maxDelayQ:qInt(5n) }
  );
  assert.equal(r.verdict, 'SHAPED');
  assert.equal(r.shaped.rateQ, qInt(5n));
  assert.equal(r.shaped.burstQ, qInt(6n));
});

test('detects impossible deadline below service latency', () => {
  const r = synthesizeShaper({ burstQ:qInt(1n), rateQ:qInt(1n) }, { rateQ:qInt(5n), latencyQ:qInt(3n) }, { maxDelayQ:qInt(2n) });
  assert.equal(r.verdict, 'IMPOSSIBLE');
});
