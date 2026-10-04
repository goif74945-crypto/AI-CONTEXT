import test from 'node:test';
import assert from 'node:assert/strict';
import { compileIdempotency, classifyReplay } from '../../../dist/concepts/01-idempotency-scope-compiler/src/index.js';

const identity=(o={})=>({route:'/api/vault/commit',actorId:'u1',projectId:'p1',authorityEpoch:'law-7',payload:{revision:2,artifact:'a'},userKey:'key-1',...o});
const policy=(o={})=>({scopeFields:['route','projectId','actorId','authorityEpoch','payload'],requirePayloadBinding:true,requireAuthorityEpoch:true,...o});

test('ISC compiles stable identity independent of object key order',()=>{
 const a=compileIdempotency(identity({payload:{artifact:'a',revision:2}}),policy());
 const b=compileIdempotency(identity({payload:{revision:2,artifact:'a'}}),policy());
 assert.equal(a.effectIdentity,b.effectIdentity);
});

test('ISC rejects policy that does not bind payload when required',()=>{
 assert.throws(()=>compileIdempotency(identity(),policy({scopeFields:['route','projectId','authorityEpoch']})),/payload must be bound/);
});

test('ISC requires route and project scope',()=>{
 assert.throws(()=>compileIdempotency(identity(),policy({scopeFields:['payload','authorityEpoch']})),/route and projectId/);
});

test('replay of same semantic payload is recognized',()=>{
 const c=compileIdempotency(identity(),policy());
 const first=classifyReplay(c,identity().payload,[]);
 assert.equal(first.verdict,'NEW');
 const second=classifyReplay(c,identity().payload,[{effectIdentity:c.effectIdentity,semanticSeal:first.semanticSeal,executionState:'COMPLETED'}]);
 assert.equal(second.verdict,'REPLAY_COMPLETED');
});

test('same effect identity with different semantic payload freezes alias',()=>{
 const c=compileIdempotency(identity(),policy());
 const old=classifyReplay(c,{revision:2},[]);
 const next=classifyReplay(c,{revision:3},[{effectIdentity:c.effectIdentity,semanticSeal:old.semanticSeal,executionState:'COMPLETED'}]);
 assert.equal(next.verdict,'FREEZE_ALIAS');
});


test('replay state distinguishes in-flight from retryable failure',()=>{
 const c=compileIdempotency(identity(),policy());
 const first=classifyReplay(c,identity().payload,[]);
 assert.equal(classifyReplay(c,identity().payload,[{effectIdentity:c.effectIdentity,semanticSeal:first.semanticSeal,executionState:'IN_FLIGHT'}]).verdict,'REPLAY_IN_FLIGHT');
 assert.equal(classifyReplay(c,identity().payload,[{effectIdentity:c.effectIdentity,semanticSeal:first.semanticSeal,executionState:'FAILED_RETRYABLE'}]).verdict,'RETRY_SAME');
});

test('duplicate registry identity fails closed',()=>{
 const c=compileIdempotency(identity(),policy());
 const first=classifyReplay(c,identity().payload,[]);
 const row={effectIdentity:c.effectIdentity,semanticSeal:first.semanticSeal,executionState:'COMPLETED'};
 assert.throws(()=>classifyReplay(c,identity().payload,[row,row]),/duplicate effect identity/);
});
