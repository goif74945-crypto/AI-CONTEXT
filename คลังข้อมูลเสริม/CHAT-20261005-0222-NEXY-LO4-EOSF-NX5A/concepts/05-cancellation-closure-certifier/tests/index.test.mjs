import test from 'node:test';
import assert from 'node:assert/strict';
import { certifyCancellationClosure } from '../../../dist/concepts/05-cancellation-closure-certifier/src/index.js';

const job=(id,parentId,state,o={})=>({id,parentId,state,hasExternalEffect:false,compensationId:null,...o});

test('CCC cancels queued/running descendants and records compensation obligations',()=>{
 const r=certifyCancellationClosure('root',[
  job('root',null,'RUNNING'),
  job('a','root','QUEUED'),
  job('b','root','SUCCEEDED',{hasExternalEffect:true,compensationId:'undo-b'}),
  job('c','a','RUNNING')
 ]);
 assert.equal(r.verdict,'PASS');
 assert.deepEqual(r.cancelNow,['a','c','root']);
 assert.deepEqual(r.requiredCompensations,['undo-b']);
});

test('CCC freezes completed external effect with no compensation',()=>{
 const r=certifyCancellationClosure('root',[job('root',null,'SUCCEEDED',{hasExternalEffect:true})]);
 assert.equal(r.verdict,'FREEZE');
 assert.deepEqual(r.blockers,['UNCOMPENSATED_EFFECT:root']);
});

test('CCC ignores jobs outside requested subtree',()=>{
 const r=certifyCancellationClosure('a',[job('root',null,'RUNNING'),job('a','root','RUNNING'),job('sibling','root','RUNNING')]);
 assert.deepEqual(r.cancelNow,['a']);
});

test('CCC rejects unknown parent',()=>{
 assert.throws(()=>certifyCancellationClosure('a',[job('a','missing','RUNNING')]),/unknown parent/);
});


test('CCC requires compensation for materialized effect even when job FAILED',()=>{
 const r=certifyCancellationClosure('root',[job('root',null,'FAILED',{hasExternalEffect:true,compensationId:null})]);
 assert.equal(r.verdict,'FREEZE');
 assert.ok(r.blockers.includes('UNCOMPENSATED_EFFECT:root'));
});

test('CCC requires compensation for materialized effect while RUNNING',()=>{
 const r=certifyCancellationClosure('root',[job('root',null,'RUNNING',{hasExternalEffect:true,compensationId:'undo-root'})]);
 assert.equal(r.verdict,'PASS');
 assert.deepEqual(r.cancelNow,['root']);
 assert.deepEqual(r.requiredCompensations,['undo-root']);
});
