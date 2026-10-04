import { preflightExternalEffect, acquireNextLease } from '../../dist/src/index.js';
const input={
 mutation:{route:'/api/vault/commit',actorId:'owner',projectId:'p',authorityEpoch:'law-7',payload:{z:3,a:1},userKey:'K'},
 idempotencyPolicy:{scopeFields:['payload','projectId','route','authorityEpoch','actorId'],requirePayloadBinding:true,requireAuthorityEpoch:true},seenMutations:[],
 retryRootId:'root',retryNodes:[{id:'root',maxAttempts:1,fanOut:1,localEffectsPerAttempt:1,retryExplicitlySafe:false,children:[]}],retryBudget:1n,
 lease:acquireNextLease(null,'vault:a','worker',20),commitAttempt:{resourceId:'vault:a',workerId:'worker',observedFence:1,atSeq:10},existingEffect:null,effectSeq:10,
 cancellationRootId:'job',jobs:[{id:'job',parentId:null,state:'RUNNING',hasExternalEffect:false,compensationId:null}]
};
const r=preflightExternalEffect(input);
console.log(JSON.stringify(r));
