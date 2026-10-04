import assert from 'node:assert/strict';
import { analyzeRetryAmplification, acquireNextLease, authorizeCommit, prepareEffect, commitEffect, emitEffect, compileIdempotency, classifyReplay, certifyCancellationClosure } from '../../dist/src/index.js';

let checks=0;
for(let i=1;i<=10000;i++){
  const lease=acquireNextLease(null,`r${i}`,`w${i}`,i+5);
  assert.equal(authorizeCommit(lease,{resourceId:`r${i}`,workerId:`w${i}`,observedFence:1,atSeq:i}).verdict,'ALLOW'); checks++;
  assert.equal(authorizeCommit(lease,{resourceId:`r${i}`,workerId:`w${i}`,observedFence:2,atSeq:i}).verdict,'FREEZE'); checks++;
}
for(let i=0;i<10000;i++){
  const r=analyzeRetryAmplification('r',[{id:'r',maxAttempts:2,fanOut:3,localEffectsPerAttempt:1,retryExplicitlySafe:true,children:['c']},{id:'c',maxAttempts:2,fanOut:1,localEffectsPerAttempt:1,retryExplicitlySafe:true,children:[]}],14n);
  assert.equal(r.verdict,'PASS'); assert.equal(r.worstCaseEffectAttempts,'14'); checks++;
}
for(let i=0;i<10000;i++){
  let r=prepareEffect(`e${i}`,{i},i); r=commitEffect(r,i+1); const first=emitEffect(r,i+2).record; const second=emitEffect(first,i+3);
  assert.equal(second.verdict,'ALREADY_EMITTED'); assert.equal(second.record.emittedSeq,i+2); checks++;
}
const policy={scopeFields:['route','actorId','projectId','authorityEpoch','payload'],requirePayloadBinding:true,requireAuthorityEpoch:true};
for(let i=0;i<5000;i++){
  const m={route:'/x',actorId:'a',projectId:'p',authorityEpoch:'e',payload:{i},userKey:`k${i}`};
  const c=compileIdempotency(m,policy); const fresh=classifyReplay(c,m.payload,[]); assert.equal(fresh.verdict,'NEW');
  const done=classifyReplay(c,m.payload,[{effectIdentity:c.effectIdentity,semanticSeal:fresh.semanticSeal,executionState:'COMPLETED'}]); assert.equal(done.verdict,'REPLAY_COMPLETED'); checks+=2;
}
for(let i=0;i<5000;i++){
  const jobs=[{id:'r',parentId:null,state:'RUNNING',hasExternalEffect:false,compensationId:null},{id:'a',parentId:'r',state:'SUCCEEDED',hasExternalEffect:true,compensationId:`undo-${i}`}];
  const a=certifyCancellationClosure('r',jobs); const b=certifyCancellationClosure('r',[jobs[1],jobs[0]]); assert.deepEqual(a,b); assert.equal(a.verdict,'PASS'); checks++;
}
console.log(JSON.stringify({stress_checks:checks,status:'PASS'}));
