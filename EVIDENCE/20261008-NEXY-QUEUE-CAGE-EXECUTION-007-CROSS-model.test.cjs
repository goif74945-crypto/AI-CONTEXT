'use strict';
const test=require('node:test');const assert=require('node:assert/strict');
function gate(){let unblock;const promise=new Promise(r=>{unblock=r});return {promise,unblock};}
function row(){return {id:'d1',status:'PENDING',attempts:0,lastError:null};}
function updateById(db,status){db.status=status;db.attempts++;}
function updateCAS(db,expected,status){if(db.status!==expected.status||db.attempts!==expected.attempts)return 0;db.status=status;db.attempts++;return 1;}
async function scenario({cas,throws}){const db=row(),entered=gate(),resume=gate(),expected={...db};let redisPublished=false;const producer=(async()=>{try{entered.unblock();await resume.promise;if(throws)throw Object.assign(new Error('redis down'),{code:'QUEUE_UNAVAILABLE'});redisPublished=true;if(cas)updateCAS(db,expected,'ENQUEUED');else updateById(db,'ENQUEUED');}catch{if(cas)updateCAS(db,expected,'FAILED');else updateById(db,'FAILED');}})();await entered.promise;db.status='CANCELLED';db.lastError='OWNER_CANCEL';resume.unblock();await producer;return {db,redisPublished};}
test('old ID-only success overwrites CANCELLED',async()=>{const {db,redisPublished}=await scenario({cas:false,throws:false});assert.equal(db.status,'ENQUEUED');assert.equal(redisPublished,true)});
test('old ID-only failure overwrites CANCELLED',async()=>{const {db}=await scenario({cas:false,throws:true});assert.equal(db.status,'FAILED')});
test('candidate CAS retains CANCELLED after Redis publication',async()=>{const {db,redisPublished}=await scenario({cas:true,throws:false});assert.equal(db.status,'CANCELLED');assert.equal(db.attempts,0);assert.equal(db.lastError,'OWNER_CANCEL');assert.equal(redisPublished,true)});
test('candidate CAS retains CANCELLED after enqueue error',async()=>{const {db}=await scenario({cas:true,throws:true});assert.equal(db.status,'CANCELLED');assert.equal(db.attempts,0)});
test('worker guarded claim rejects CANCELLED',()=>{const db={status:'CANCELLED'};assert.equal(['PENDING','ENQUEUED'].includes(db.status),false)});
