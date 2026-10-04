import test from 'node:test';
import assert from 'node:assert/strict';
import { prepareEffect, reconcilePrepared, commitEffect, emitEffect, cancelPrepared, auditEffectRecord } from '../../../dist/concepts/04-outbox-effect-seal/src/index.js';

test('OES enforces PREPARED -> COMMITTED -> EMITTED',()=>{
 let r=prepareEffect('e1',{kind:'email',to:'x'},1);
 r=commitEffect(r,2);
 const e=emitEffect(r,3);
 assert.equal(e.verdict,'EMIT');
 assert.equal(e.record.state,'EMITTED');
 assert.deepEqual(auditEffectRecord(e.record),[]);
});

test('OES makes repeated emission idempotent',()=>{
 const emitted=emitEffect(commitEffect(prepareEffect('e1',{x:1},1),2),3).record;
 const again=emitEffect(emitted,4);
 assert.equal(again.verdict,'ALREADY_EMITTED');
 assert.equal(again.record.emittedSeq,3);
});

test('OES freezes same effect id with different payload',()=>{
 const a=prepareEffect('e1',{amount:10},1);
 const b=prepareEffect('e1',{amount:11},1);
 assert.equal(reconcilePrepared(a,b).verdict,'FREEZE_CONFLICT');
});

test('OES forbids emission before commit',()=>{
 assert.throws(()=>emitEffect(prepareEffect('e1',{x:1},1),2),/COMMITTED/);
});

test('OES permits cancel only before commit',()=>{
 assert.equal(cancelPrepared(prepareEffect('e1',{x:1},1)).state,'CANCELLED');
 assert.throws(()=>cancelPrepared(commitEffect(prepareEffect('e2',{x:1},1),2)),/only PREPARED/);
});

test('OES audit detects tampering',()=>{
 const r=prepareEffect('e1',{x:1},1);
 const forged={...r,payload:{x:2}};
 assert.ok(auditEffectRecord(forged).includes('PAYLOAD_SEAL_MISMATCH'));
});

test('OES reconciles exact state and refuses reuse after cancellation',()=>{
 const prepared=prepareEffect('e1',{x:1},1);
 assert.equal(reconcilePrepared(prepared,prepareEffect('e1',{x:1},2)).verdict,'REPLAY_PREPARED');
 const committed=commitEffect(prepared,2);
 assert.equal(reconcilePrepared(committed,prepareEffect('e1',{x:1},3)).verdict,'REPLAY_COMMITTED');
 const emitted=emitEffect(committed,3).record;
 assert.equal(reconcilePrepared(emitted,prepareEffect('e1',{x:1},4)).verdict,'REPLAY_EMITTED');
 const cancelled=cancelPrepared(prepared);
 assert.equal(reconcilePrepared(cancelled,prepareEffect('e1',{x:1},5)).verdict,'FREEZE_CANCELLED');
});
