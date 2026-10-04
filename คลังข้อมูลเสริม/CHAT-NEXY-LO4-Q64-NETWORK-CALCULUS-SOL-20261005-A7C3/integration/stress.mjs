import test from 'node:test';
import assert from 'node:assert/strict';
import { qInt } from '../dist/shared/q64.js';
import { certifyFlow } from '../dist/01_FLOWGUARD_64/src.js';
import { certifyBacklog } from '../dist/02_QUEUEBOUND_64/src.js';
import { certifyDeadline } from '../dist/03_DEADLINE_64/src.js';

test('bounded deterministic corpus preserves stability and monotonic bounds', () => {
  let cases = 0;
  for (let b = 0n; b <= 20n; b++) {
    for (let r = 0n; r <= 8n; r++) {
      for (let extra = 0n; extra <= 4n; extra++) {
        const R = r + 1n + extra;
        for (let T = 0n; T <= 5n; T++) {
          const arrival={burstQ:qInt(b),rateQ:qInt(r)};
          const service={rateQ:qInt(R),latencyQ:qInt(T)};
          const f1=certifyFlow(arrival,service);
          const f2=certifyFlow(arrival,service);
          assert.equal(f1.verdict,'ADMIT');
          assert.equal(f1.fingerprint,f2.fingerprint);
          const b0=certifyBacklog(arrival,service);
          const b1=certifyBacklog({burstQ:qInt(b+1n),rateQ:qInt(r)},service);
          assert.equal(b1.backlogBoundQ >= b0.backlogBoundQ,true);
          const d0=certifyDeadline(arrival,service);
          const d1=certifyDeadline({burstQ:qInt(b+1n),rateQ:qInt(r)},service);
          assert.equal(d1.delayBoundQ >= d0.delayBoundQ,true);
          cases++;
        }
      }
    }
  }
  assert.equal(cases, 21*9*5*6);
});
