import test from 'node:test';
import assert from 'node:assert/strict';
import { acquireNextLease, authorizeCommit } from '../../../dist/concepts/03-lease-fencing-commit-gate/src/index.js';

test('LFCG allows current holder with exact fence',()=>{
 const lease=acquireNextLease(null,'artifact:a','worker-1',20);
 assert.deepEqual(authorizeCommit(lease,{resourceId:'artifact:a',workerId:'worker-1',observedFence:1,atSeq:20}),{verdict:'ALLOW',fence:1});
});

test('LFCG rejects stale worker after re-acquisition',()=>{
 const first=acquireNextLease(null,'artifact:a','worker-old',10);
 const next=acquireNextLease(first,'artifact:a','worker-new',30);
 assert.deepEqual(authorizeCommit(next,{resourceId:'artifact:a',workerId:'worker-old',observedFence:1,atSeq:9}),{verdict:'FREEZE',reason:'WRONG_HOLDER'});
 assert.deepEqual(authorizeCommit(next,{resourceId:'artifact:a',workerId:'worker-new',observedFence:1,atSeq:9}),{verdict:'FREEZE',reason:'STALE_FENCE'});
});

test('LFCG rejects future fence and expired lease',()=>{
 const lease=acquireNextLease(null,'r','w',5);
 assert.equal(authorizeCommit(lease,{resourceId:'r',workerId:'w',observedFence:2,atSeq:1}).reason,'FUTURE_FENCE');
 assert.equal(authorizeCommit(lease,{resourceId:'r',workerId:'w',observedFence:1,atSeq:6}).reason,'LEASE_EXPIRED');
});

test('LFCG rejects revoked lease',()=>{
 const lease={...acquireNextLease(null,'r','w',5),revoked:true};
 assert.equal(authorizeCommit(lease,{resourceId:'r',workerId:'w',observedFence:1,atSeq:1}).reason,'REVOKED');
});
