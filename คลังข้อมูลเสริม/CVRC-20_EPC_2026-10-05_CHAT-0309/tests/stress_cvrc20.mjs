import assert from "node:assert/strict";
import { NEXY_BASELINE, cloneBaseline } from "../src/baseline.mjs";
import { evaluateAll, GATE_IDS, summarizeDeterministically } from "../src/gates.mjs";

let seed=0x9e615b04n;
function next(){seed ^= seed<<13n;seed ^= seed>>7n;seed ^= seed<<17n;seed &= (1n<<64n)-1n;return seed;}
function pick(n){return Number(next()%BigInt(n));}
const mutations=[
 c=>{c.release.quorumMin=1;},
 c=>{c.release.confidenceMinQ64=0n;},
 c=>{c.rbac.manage_roles.push("PUBLIC_USER");},
 c=>{c.queue.revalidateBeforeConsume=false;},
 c=>{c.vault.appendOnlyRevisions=false;},
 c=>{c.uiTruth.optimisticBlockingSuccess=true;},
 c=>{c.numericScopes.GAME_G15.overflow="FREEZE";},
 c=>{c.numericScopes.CORE_L9.overflow="SATURATE";},
 c=>{c.envelope.statuses=c.envelope.statuses.filter(x=>x!=="FREEZE");},
 c=>{c.errorCodes.vnext=c.errorCodes.vnext.filter(x=>x!=="WAL_INTEGRITY_FAILURE");},
 c=>{c.adapter.requiredFields=c.adapter.requiredFields.filter(x=>x!=="deterministic_capable");},
 c=>{c.observability.orphanIncidentForbidden=false;},
 c=>{c.config.immutableAtRuntime=c.config.immutableAtRuntime.filter(x=>x!=="state_machine_definition");},
 c=>{c.transitions.find(t=>t.from==="FREEZE"&&t.event==="recover").owners.push("API");},
 c=>{c.transitions.push({from:"INIT",event:"accepted",to:"STABLE",owners:["JUDGE"],guards:["not_in_stop"]});}
];
let iterations=5000,rejected=0,deterministicMatches=0;
for(let i=0;i<iterations;i++){
  const c=cloneBaseline();
  const count=1+pick(4);
  for(let j=0;j<count;j++) mutations[pick(mutations.length)](c);
  const r1=evaluateAll(NEXY_BASELINE,c);
  const r2=evaluateAll(NEXY_BASELINE,structuredClone(c));
  const s1=summarizeDeterministically(r1),s2=summarizeDeterministically(r2);
  assert.equal(s1.hash,s2.hash); deterministicMatches++;
  assert.equal(r1.composite.verdict,"REJECT");
  assert.ok(r1.composite.failedGateIds.length>=1); rejected++;
}
assert.equal(new Set(GATE_IDS).size,20);
console.log(JSON.stringify({status:"PASS",suite:"cvrc20-stress",iterations,rejected,deterministicMatches,seedFinal:seed.toString(16)}));
