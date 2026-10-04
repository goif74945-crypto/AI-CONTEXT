import assert from "node:assert/strict";
import { NEXY_BASELINE, cloneBaseline } from "../src/baseline.mjs";
import { evaluateAll, GATE_IDS, summarizeDeterministically } from "../src/gates.mjs";
import { evaluatePromotionCandidate } from "../src/integration.mjs";
import { I128_MAX, I128_MIN, Q64_ONE, q64Add, q64Div, q64FromRatio, q64Mul, Q64RangeError, Q64DivisionByZeroError } from "../src/q64.mjs";

let assertions=0;
const ok=(v,msg)=>{assert.ok(v,msg);assertions++;};
const eq=(a,b,msg)=>{assert.deepEqual(a,b,msg);assertions++;};
function mutation(mutator){const c=cloneBaseline();mutator(c);return c;}
function gate(report,id){return report.gates.find(g=>g.id===id);}

{
  const report=evaluateAll(NEXY_BASELINE,cloneBaseline());
  eq(report.gates.length,20,"exactly 20 CVRC systems");
  eq(report.gates.map(g=>g.id),GATE_IDS,"stable gate ordering");
  eq(report.composite.verdict,"KEEP_CANDIDATE");
  eq(report.composite.status,"PASS");
  eq(report.composite.canPromoteCanon,false);
  eq(report.composite.canMutateCoreState,false);
  eq(report.composite.canWriteVault,false);
}
const cases=[
  [GATE_IDS[0], c=>{c.states=c.states.filter(x=>x!=="FREEZE");}],
  [GATE_IDS[1], c=>{c.transitions=c.transitions.filter(t=>!(t.from==="READY"&&t.event==="execute"));}],
  [GATE_IDS[2], c=>{c.transitions.push({from:"READY",event:"accepted",to:"STABLE",owners:["JUDGE"],guards:["not_in_stop"]});}],
  [GATE_IDS[3], c=>{c.transitions.find(t=>t.event==="agents_done").owners.push("API");}],
  [GATE_IDS[4], c=>{const t=c.transitions.find(t=>t.from==="CONSENSUS"&&t.event==="accepted");t.guards=t.guards.filter(x=>x!=="release_policy_passed");}],
  [GATE_IDS[5], c=>{c.transitions.find(t=>t.from==="RUNNING"&&t.event==="error").to="READY";}],
  [GATE_IDS[6], c=>{c.freezeRecovery.HASH_DIVERGENCE={recoverable:true,actors:["OWNER"]};}],
  [GATE_IDS[7], c=>{c.release.evidenceMin=1;}],
  [GATE_IDS[8], c=>{c.release.requiredBooleanGates=c.release.requiredBooleanGates.filter(x=>x!=="law_pre_release_passed");}],
  [GATE_IDS[9], c=>{c.rbac.manage_roles.push("OPERATOR");}],
  [GATE_IDS[10],c=>{c.forbiddenModuleEdges=c.forbiddenModuleEdges.filter(x=>x!=="JUDGE->CORE");}],
  [GATE_IDS[11],c=>{c.envelope.requiredFields=c.envelope.requiredFields.filter(x=>x!=="trace_id");}],
  [GATE_IDS[12],c=>{c.errorCodes.api=c.errorCodes.api.filter(x=>x!=="STATE_TRANSITION_DENIED");}],
  [GATE_IDS[13],c=>{c.numericScopes.CORE_L9.overflow="SATURATE";}],
  [GATE_IDS[14],c=>{c.queue.autoRetryDefault=true;}],
  [GATE_IDS[15],c=>{c.vault.overwriteRevisionForbidden=false;}],
  [GATE_IDS[16],c=>{c.adapter.requiredMethods=c.adapter.requiredMethods.filter(x=>x!=="cancel");}],
  [GATE_IDS[17],c=>{c.evidence.requiredFields=c.evidence.requiredFields.filter(x=>x!=="verified");}],
  [GATE_IDS[18],c=>{c.uiTruth.mayMaskFreeze=true;}]
];
for(const [id,mutator] of cases){
  const report=evaluateAll(NEXY_BASELINE,mutation(mutator));
  eq(gate(report,id).status,"FAIL",`${id} must reject its targeted regression`);
  eq(report.composite.verdict,"REJECT",`${id} must block KEEP recommendation`);
  ok(report.composite.failedGateIds.includes(id),`${id} must be named in failure evidence`);
}
{
  const c=cloneBaseline(); delete c.evidence;
  const report=evaluateAll(NEXY_BASELINE,c);
  eq(gate(report,GATE_IDS[17]).status,"NOT_VERIFIED");
  eq(report.composite.verdict,"DEFER");
}
{
  const good=evaluatePromotionCandidate(NEXY_BASELINE,cloneBaseline(),{nexyCommit:NEXY_BASELINE.identity.commit});
  eq(good.release,"KEEP_CANDIDATE");
  eq(good.authority,"NONE"); eq(good.nextAuthority,"JUDGE_LAW_REVIEW_REQUIRED");
  eq(good.canPromoteCanon,false); eq(good.canMutateCoreState,false); eq(good.canWriteVault,false);
  const stale=evaluatePromotionCandidate(NEXY_BASELINE,cloneBaseline(),{nexyCommit:"0".repeat(40)});
  eq(stale.release,"DEFER"); eq(stale.reason,"TARGET_COMMIT_MISMATCH");
}
{
  const a=summarizeDeterministically(evaluateAll(NEXY_BASELINE,cloneBaseline()));
  const b=summarizeDeterministically(evaluateAll(NEXY_BASELINE,cloneBaseline()));
  eq(a,b); eq(a.hash.length,64);
}
{
  eq(q64FromRatio(1n,2n),1n<<63n);
  eq(q64FromRatio(3n,4n),3n<<62n);
  eq(q64Mul(q64FromRatio(3n,2n),q64FromRatio(2n,3n)),Q64_ONE-1n);
  eq(q64Div(Q64_ONE,2n*Q64_ONE),1n<<63n);
  assert.throws(()=>q64Add(I128_MAX,1n),Q64RangeError); assertions++;
  assert.throws(()=>q64Div(Q64_ONE,0n),Q64DivisionByZeroError); assertions++;
  ok(I128_MIN<0n && I128_MAX>0n);
}
console.log(JSON.stringify({status:"PASS",suite:"cvrc20-unit",gates:20,targetCommit:NEXY_BASELINE.identity.commit,assertions}));
