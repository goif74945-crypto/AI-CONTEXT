import assert from "node:assert/strict";
import { s01Fingerprint,s11Replay,s18RollbackCapsule } from "../src/fabric.mjs";
import { qFromInt,qSerialize } from "../src/q64.mjs";
const base={id:"x",provider:"p",schema_version:"7.0.0",supported_modes:["fast","strict","audit"],deterministic_capable:false,critical:true,max_context_raw:qSerialize(qFromInt(8192n))};
const first=s01Fingerprint(base).evidence.fingerprint;
for(let i=0;i<5000;i++){
  const modes=i%2?["audit","fast","strict"]:["strict","audit","fast"];
  assert.equal(s01Fingerprint({...base,supported_modes:modes}).evidence.fingerprint,first);
  assert.equal(s11Replay([{x:"1",y:"2"},{y:"2",x:"1"}]).status,"PASS");
  const a=s18RollbackCapsule([{id:"b",provider:"g",fingerprint:"2"},{id:"a",provider:"o",fingerprint:"1"}],{nexy:"n",spec:"s"}).evidence.rollback_hash;
  const b=s18RollbackCapsule([{id:"a",provider:"o",fingerprint:"1"},{id:"b",provider:"g",fingerprint:"2"}],{nexy:"n",spec:"s"}).evidence.rollback_hash;
  assert.equal(a,b);
}
console.log(JSON.stringify({status:"PASS",iterations:5000,checks:15000}));
