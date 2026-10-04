import test from 'node:test';
import assert from 'node:assert/strict';
import { preflightExternalEffect, acquireNextLease, prepareEffect, compileIdempotency, classifyReplay } from '../../dist/src/index.js';

function good(overrides={}) {
 const mutation={route:'/api/vault/commit',actorId:'owner',projectId:'p',authorityEpoch:'law-7',payload:{artifact:'a',revision:2},userKey:'K'};
 const base={
  mutation,
  idempotencyPolicy:{scopeFields:['route','actorId','projectId','authorityEpoch','payload'],requirePayloadBinding:true,requireAuthorityEpoch:true},
  seenMutations:[],
  retryRootId:'root',retryNodes:[{id:'root',maxAttempts:1,fanOut:1,localEffectsPerAttempt:1,retryExplicitlySafe:false,children:[]}],retryBudget:1n,
  lease:acquireNextLease(null,'vault:a','worker',20),commitAttempt:{resourceId:'vault:a',workerId:'worker',observedFence:1,atSeq:10},
  existingEffect:null,effectSeq:10,
  cancellationRootId:'job',jobs:[{id:'job',parentId:null,state:'RUNNING',hasExternalEffect:false,compensationId:null}],
 };
 return {...base,...overrides};
}

test('integration READY when all five gates pass',()=>{
 const r=preflightExternalEffect(good());
 assert.equal(r.verdict,'READY');
 assert.equal(r.retryWorstCase,'1');
 assert.deepEqual(r.cancellations,['job']);
});

test('integration aggregates independent blockers instead of first-error hiding',()=>{
 const g=good();
 const r=preflightExternalEffect(good({
  retryNodes:[{id:'root',maxAttempts:2,fanOut:1,localEffectsPerAttempt:2,retryExplicitlySafe:false,children:[]}],retryBudget:1n,
  commitAttempt:{...g.commitAttempt,observedFence:2},
  jobs:[{id:'job',parentId:null,state:'SUCCEEDED',hasExternalEffect:true,compensationId:null}]
 }));
 assert.equal(r.verdict,'FREEZE');
 assert.ok(r.blockers.includes('RETRY:RETRY_NOT_EXPLICITLY_SAFE'));
 assert.ok(r.blockers.includes('RETRY:EFFECT_ATTEMPT_BUDGET_EXCEEDED'));
 assert.ok(r.blockers.includes('FENCE:FUTURE_FENCE'));
 assert.ok(r.blockers.includes('CANCEL:UNCOMPENSATED_EFFECT:job'));
});

test('integration detects outbox payload conflict for same effect identity',()=>{
 const first=preflightExternalEffect(good());
 assert.equal(first.verdict,'READY');
 const conflict=prepareEffect(first.effectIdentity,{artifact:'different'},10);
 const r=preflightExternalEffect(good({existingEffect:conflict}));
 assert.equal(r.verdict,'FREEZE');
 assert.ok(r.blockers.includes('OUTBOX:PAYLOAD_MISMATCH'));
});


test('integration suppresses a completed idempotent replay instead of re-executing effect',()=>{
 const g=good();
 const compiled=compileIdempotency(g.mutation,g.idempotencyPolicy);
 const digest=classifyReplay(compiled,g.mutation.payload,[]).semanticSeal;
 const r=preflightExternalEffect(good({seenMutations:[{effectIdentity:compiled.effectIdentity,semanticSeal:digest,executionState:'COMPLETED'}]}));
 assert.deepEqual(r,{verdict:'SUPPRESS_REPLAY',effectIdentity:compiled.effectIdentity,evidence:'REGISTRY_COMPLETED'});
});

test('integration freezes in-flight duplicate and allows retryable duplicate only through retry gate',()=>{
 const g=good();
 const compiled=compileIdempotency(g.mutation,g.idempotencyPolicy);
 const digest=classifyReplay(compiled,g.mutation.payload,[]).semanticSeal;
 const inFlight=preflightExternalEffect(good({seenMutations:[{effectIdentity:compiled.effectIdentity,semanticSeal:digest,executionState:'IN_FLIGHT'}]}));
 assert.equal(inFlight.verdict,'FREEZE');
 assert.ok(inFlight.blockers.includes('IDEMPOTENCY_IN_FLIGHT'));
 const retry=preflightExternalEffect(good({
   seenMutations:[{effectIdentity:compiled.effectIdentity,semanticSeal:digest,executionState:'FAILED_RETRYABLE'}],
   retryNodes:[{id:'root',maxAttempts:2,fanOut:1,localEffectsPerAttempt:1,retryExplicitlySafe:true,children:[]}],
   retryBudget:2n
 }));
 assert.equal(retry.verdict,'READY');
});

test('integration suppresses replay when outbox already emitted even if registry row is absent',()=>{
 const g=good();
 const first=preflightExternalEffect(g);
 assert.equal(first.verdict,'READY');
 const emitted={...first.effectRecord,state:'EMITTED',committedSeq:11,emittedSeq:12};
 const r=preflightExternalEffect(good({existingEffect:emitted}));
 assert.equal(r.verdict,'SUPPRESS_REPLAY');
 assert.equal(r.evidence,'OUTBOX_EMITTED');
});

test('integration freezes registry/outbox state contradiction',()=>{
 const g=good();
 const compiled=compileIdempotency(g.mutation,g.idempotencyPolicy);
 const seal=classifyReplay(compiled,g.mutation.payload,[]).semanticSeal;
 const prepared=prepareEffect(compiled.effectIdentity,g.mutation.payload,10);
 const r=preflightExternalEffect(good({seenMutations:[{effectIdentity:compiled.effectIdentity,semanticSeal:seal,executionState:'COMPLETED'}],existingEffect:prepared}));
 assert.equal(r.verdict,'FREEZE');
 assert.ok(r.blockers.includes('REGISTRY_OUTBOX_STATE_CONFLICT'));
});

test('integration resumes from COMMITTED outbox record without creating a second effect identity',()=>{
 const g=good();
 const first=preflightExternalEffect(g);
 assert.equal(first.verdict,'READY');
 const committed={...first.effectRecord,state:'COMMITTED',committedSeq:11};
 const r=preflightExternalEffect(good({existingEffect:committed}));
 assert.equal(r.verdict,'READY');
 assert.equal(r.resumeFrom,'COMMITTED');
 assert.equal(r.effectIdentity,first.effectIdentity);
});
