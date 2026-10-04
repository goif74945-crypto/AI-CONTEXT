import test from 'node:test';
import assert from 'node:assert/strict';
import { analyzeRetryAmplification } from '../../../dist/concepts/02-retry-amplification-bounder/src/index.js';

const node=(id,o={})=>({id,maxAttempts:1,fanOut:1,localEffectsPerAttempt:0,retryExplicitlySafe:false,children:[],...o});

test('RAB computes worst-case nested retry amplification',()=>{
 const r=analyzeRetryAmplification('root',[
  node('root',{maxAttempts:2,retryExplicitlySafe:true,children:['child'],fanOut:3,localEffectsPerAttempt:1}),
  node('child',{maxAttempts:2,retryExplicitlySafe:true,localEffectsPerAttempt:1})
 ],20n);
 assert.equal(r.worstCaseEffectAttempts,'14');
 assert.equal(r.verdict,'PASS');
});

test('RAB freezes retry when explicit safe flag is absent',()=>{
 const r=analyzeRetryAmplification('root',[node('root',{maxAttempts:2,localEffectsPerAttempt:1})],10n);
 assert.equal(r.verdict,'FREEZE');
 assert.deepEqual(r.unsafeRetryNodes,['root']);
});

test('RAB freezes if worst-case effects exceed budget',()=>{
 const r=analyzeRetryAmplification('root',[node('root',{maxAttempts:3,retryExplicitlySafe:true,localEffectsPerAttempt:2})],5n);
 assert.ok(r.reasonCodes.includes('EFFECT_ATTEMPT_BUDGET_EXCEEDED'));
});

test('RAB rejects cycles',()=>{
 assert.throws(()=>analyzeRetryAmplification('a',[node('a',{children:['b']}),node('b',{children:['a']})],100n),/cycle/);
});

test('RAB rejects analysis cap explosion',()=>{
 assert.throws(()=>analyzeRetryAmplification('a',[node('a',{maxAttempts:1000,retryExplicitlySafe:true,fanOut:1000,children:['b']}),node('b',{maxAttempts:1000,retryExplicitlySafe:true,localEffectsPerAttempt:1000})],10_000n,1_000_000n),/cap/);
});
