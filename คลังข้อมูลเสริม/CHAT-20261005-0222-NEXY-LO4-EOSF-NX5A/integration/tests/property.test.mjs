import test from 'node:test';
import assert from 'node:assert/strict';
import { compileIdempotency, analyzeRetryAmplification, acquireNextLease, authorizeCommit, prepareEffect, commitEffect, emitEffect, certifyCancellationClosure } from '../../dist/src/index.js';

function rng(seed){let s=BigInt(seed);return()=>{s=(1103515245n*s+12345n)%2147483648n;return Number(s)/2147483648;};}

test('property: idempotency scope is invariant to payload key insertion order for 100 cases',()=>{
 const p={scopeFields:['route','actorId','projectId','authorityEpoch','payload'],requirePayloadBinding:true,requireAuthorityEpoch:true};
 for(let i=0;i<100;i++){
  const a={route:'/m',actorId:'a',projectId:'p',authorityEpoch:'e',payload:{x:i,y:i+1},userKey:'k'};
  const b={...a,payload:{y:i+1,x:i}};
  assert.equal(compileIdempotency(a,p).effectIdentity,compileIdempotency(b,p).effectIdentity);
 }
});

test('property: stale fences never authorize after 500 reacquisitions',()=>{
 let lease=null;
 for(let i=1;i<=500;i++){
  lease=acquireNextLease(lease,'r',`w${i}`,1000+i);
  if(i>1){
    const d=authorizeCommit(lease,{resourceId:'r',workerId:`w${i}`,observedFence:i-1,atSeq:i});
    assert.equal(d.verdict,'FREEZE');
    assert.equal(d.reason,'STALE_FENCE');
  }
 }
});

test('property: outbox repeated emit never advances original emission sequence',()=>{
 for(let i=0;i<100;i++){
   const first=emitEffect(commitEffect(prepareEffect(`e${i}`,{i},i),i+1),i+2).record;
   const again=emitEffect(first,i+1000);
   assert.equal(again.verdict,'ALREADY_EMITTED');
   assert.equal(again.record.emittedSeq,i+2);
 }
});

test('property: retry calculation matches closed form for 200 shallow cases',()=>{
 const random=rng(74945);
 for(let i=0;i<200;i++){
  const attempts=1+Math.floor(random()*5), fan=1+Math.floor(random()*4), childEff=Math.floor(random()*4), rootEff=Math.floor(random()*3);
  const nodes=[
   {id:'r',maxAttempts:attempts,fanOut:fan,localEffectsPerAttempt:rootEff,retryExplicitlySafe:true,children:['c']},
   {id:'c',maxAttempts:1,fanOut:1,localEffectsPerAttempt:childEff,retryExplicitlySafe:false,children:[]}
  ];
  const expected=BigInt(attempts*(rootEff+fan*childEff));
  const r=analyzeRetryAmplification('r',nodes,10_000n);
  assert.equal(r.worstCaseEffectAttempts,expected.toString());
 }
});

test('property: cancellation result is invariant to input ordering',()=>{
 const jobs=[
  {id:'r',parentId:null,state:'RUNNING',hasExternalEffect:false,compensationId:null},
  {id:'a',parentId:'r',state:'QUEUED',hasExternalEffect:false,compensationId:null},
  {id:'b',parentId:'r',state:'SUCCEEDED',hasExternalEffect:true,compensationId:'undo'}
 ];
 const a=certifyCancellationClosure('r',jobs);
 const b=certifyCancellationClosure('r',[jobs[2],jobs[0],jobs[1]]);
 assert.deepEqual(a,b);
});
