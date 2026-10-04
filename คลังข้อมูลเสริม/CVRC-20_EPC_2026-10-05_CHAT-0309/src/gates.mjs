import { q64RatioOfCounts, q64ComplementUnit } from "./q64.mjs";
import { setContainsAll, setIsSubset, sha256Canonical, sortedUnique } from "./canonical.mjs";

function passFail(checks) {
  const failed = checks.filter(c => !c.pass);
  const coverageQ64 = q64RatioOfCounts(checks.length - failed.length, checks.length);
  return Object.freeze({
    status: failed.length === 0 ? "PASS" : "FAIL",
    coverageQ64,
    riskQ64: q64ComplementUnit(coverageQ64),
    checks: Object.freeze(checks),
    reasons: Object.freeze(failed.map(c => c.reason))
  });
}
function missing(candidate, path) {
  const parts = path.split(".");
  let v = candidate;
  for (const p of parts) {
    if (v === undefined || v === null || !(p in Object(v))) return true;
    v = v[p];
  }
  return false;
}
function notVerified(id, missingPaths) {
  return Object.freeze({
    id, status:"NOT_VERIFIED", coverageQ64:0n, riskQ64:0n,
    checks:Object.freeze([]),
    reasons:Object.freeze(missingPaths.map(p=>`missing:${p}`))
  });
}
function wrap(id, requiredPaths, candidate, fn) {
  if (!candidate || typeof candidate !== "object") return notVerified(id, ["candidate"]);
  const absent = requiredPaths.filter(path => missing(candidate, path));
  if (absent.length) return notVerified(id, absent);
  try {
    const r = fn();
    return Object.freeze({ id, ...r });
  } catch (error) {
    const name = error && typeof error === "object" && "name" in error ? String(error.name) : "Error";
    return Object.freeze({
      id, status:"NOT_VERIFIED", coverageQ64:0n, riskQ64:0n,
      checks:Object.freeze([]), reasons:Object.freeze([`malformed:${name}`])
    });
  }
}
function keyTransition(t) { return `${t.from}|${t.event}|${t.to}`; }
function keyFromEvent(t) { return `${t.from}|${t.event}`; }
function lookupTransitions(model) { return new Map(model.transitions.map(t => [keyTransition(t), t])); }
function lookupFromEvent(model) { return new Map(model.transitions.map(t => [keyFromEvent(t), t])); }

export const GATE_IDS = Object.freeze([
  "CVRC01_STATE_UNIVERSE_PRESERVATION",
  "CVRC02_TRACE_FORWARD_SIMULATION",
  "CVRC03_ILLEGAL_TRANSITION_NONEXPANSION",
  "CVRC04_EVENT_OWNER_NONWIDENING",
  "CVRC05_GUARD_STRENGTH_MONOTONICITY",
  "CVRC06_FREEZE_STOP_DOMINANCE",
  "CVRC07_RECOVERY_AUTHORITY_NONWIDENING",
  "CVRC08_RELEASE_POLICY_MONOTONICITY",
  "CVRC09_RELEASE_GATE_PRESERVATION",
  "CVRC10_RBAC_AUTHORITY_NONWIDENING",
  "CVRC11_MODULE_BOUNDARY_NONEXPANSION",
  "CVRC12_ENVELOPE_TRUTH_PRESERVATION",
  "CVRC13_ERROR_TAXONOMY_NOLOSS",
  "CVRC14_NUMERIC_SCOPE_LAW_PRESERVATION",
  "CVRC15_QUEUE_SAFETY_MONOTONICITY",
  "CVRC16_VAULT_LINEAGE_MONOTONICITY",
  "CVRC17_ADAPTER_CONTRACT_REFINEMENT",
  "CVRC18_EVIDENCE_CONTRACT_REFINEMENT",
  "CVRC19_OBSERVABILITY_UI_CONFIG_REFINEMENT",
  "CVRC20_COMPOSITE_PROMOTION_COURT"
]);

export function gate01StateUniverse(base,candidate){
  return wrap(GATE_IDS[0],["states"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.states,base.states),reason:"candidate removed/renamed a canonical product state"},
    {pass:new Set(candidate.states).size===candidate.states.length,reason:"candidate state set contains duplicates"}
  ]));
}
export function gate02TraceForwardSimulation(base,candidate){
  return wrap(GATE_IDS[1],["transitions"],candidate,()=>{
    const c=lookupTransitions(candidate);
    return passFail(base.transitions.map(t=>({
      pass:c.has(keyTransition(t)),reason:`baseline trace step not simulated: ${keyTransition(t)}`
    })));
  });
}
export function gate03IllegalTransitionNonexpansion(base,candidate){
  return wrap(GATE_IDS[2],["transitions"],candidate,()=>{
    const b=new Set(base.transitions.map(keyTransition));
    const checks=candidate.transitions.map(t=>({
      pass:b.has(keyTransition(t)),reason:`candidate legalizes non-baseline transition: ${keyTransition(t)}`
    }));
    return passFail(checks.length?checks:[{pass:true,reason:""}]);
  });
}
export function gate04EventOwnerNonwidening(base,candidate){
  return wrap(GATE_IDS[3],["transitions"],candidate,()=>{
    const b=lookupFromEvent(base);
    return passFail(candidate.transitions.map(t=>{
      const prior=b.get(keyFromEvent(t));
      return {
        pass:!!prior && setIsSubset(t.owners,prior.owners),
        reason:`event owner widened or transition unknown: ${keyFromEvent(t)}`
      };
    }));
  });
}
export function gate05GuardStrength(base,candidate){
  return wrap(GATE_IDS[4],["transitions"],candidate,()=>{
    const c=lookupFromEvent(candidate);
    return passFail(base.transitions.map(t=>{
      const next=c.get(keyFromEvent(t));
      return {
        pass:!!next && setContainsAll(next.guards,t.guards),
        reason:`guard weakened: ${keyFromEvent(t)}`
      };
    }));
  });
}
export function gate06FreezeStopDominance(base,candidate){
  return wrap(GATE_IDS[5],["transitions"],candidate,()=>{
    const safetyEvents=new Set(["error","fatal","timeout","cancel","rejected"]);
    const rank={STOP:2,FREEZE:1};
    const c=lookupFromEvent(candidate);
    const refs=base.transitions.filter(t=>safetyEvents.has(t.event));
    return passFail(refs.map(t=>{
      const next=c.get(keyFromEvent(t));
      const baseRank=rank[t.to]??0, nextRank=next?(rank[next.to]??0):-1;
      return {
        pass:!!next && nextRank>=baseRank,
        reason:`safety destination weakened: ${keyFromEvent(t)} ${t.to}->${next?.to??"MISSING"}`
      };
    }));
  });
}
export function gate07RecoveryAuthority(base,candidate){
  return wrap(GATE_IDS[6],["freezeRecovery"],candidate,()=>{
    const checks=[];
    for(const [code,rule] of Object.entries(base.freezeRecovery)){
      const next=candidate.freezeRecovery[code];
      checks.push({pass:!!next,reason:`missing freeze rule: ${code}`});
      if(!next) continue;
      checks.push({
        pass:!(rule.recoverable===false && next.recoverable===true),
        reason:`nonrecoverable reason became recoverable: ${code}`
      });
      checks.push({
        pass:setIsSubset(next.actors,rule.actors),
        reason:`recovery actor widened: ${code}`
      });
    }
    return passFail(checks);
  });
}
export function gate08ReleasePolicy(base,candidate){
  return wrap(GATE_IDS[7],["release"],candidate,()=>passFail([
    {pass:candidate.release.confidenceMinQ64>=base.release.confidenceMinQ64,reason:"confidence threshold weakened"},
    {pass:candidate.release.deterministicMatchMinQ64>=base.release.deterministicMatchMinQ64,reason:"determinism threshold weakened"},
    {pass:candidate.release.quorumMin>=base.release.quorumMin,reason:"quorum minimum weakened"},
    {pass:candidate.release.evidenceMin>=base.release.evidenceMin,reason:"evidence minimum weakened"}
  ]));
}
export function gate09ReleaseGates(base,candidate){
  return wrap(GATE_IDS[8],["release.requiredBooleanGates"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.release.requiredBooleanGates,base.release.requiredBooleanGates),reason:"required release gate removed"}
  ]));
}
export function gate10Rbac(base,candidate){
  return wrap(GATE_IDS[9],["rbac"],candidate,()=>{
    const checks=[];
    for(const [perm,roles] of Object.entries(base.rbac)){
      const next=candidate.rbac[perm];
      checks.push({pass:Array.isArray(next),reason:`permission missing: ${perm}`});
      if(next) checks.push({pass:setIsSubset(next,roles),reason:`authority widened: ${perm}`});
    }
    return passFail(checks);
  });
}
export function gate11ModuleBoundary(base,candidate){
  return wrap(GATE_IDS[10],["forbiddenModuleEdges"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.forbiddenModuleEdges,base.forbiddenModuleEdges),reason:"a canonical forbidden dependency edge was legalized"}
  ]));
}
export function gate12Envelope(base,candidate){
  return wrap(GATE_IDS[11],["envelope"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.envelope.requiredFields,base.envelope.requiredFields),reason:"SystemEnvelope required field removed"},
    {pass:setContainsAll(candidate.envelope.statuses,base.envelope.statuses),reason:"canonical status removed"},
    {pass:setContainsAll(candidate.envelope.states,base.envelope.states),reason:"canonical state removed from envelope"}
  ]));
}
export function gate13Errors(base,candidate){
  return wrap(GATE_IDS[12],["errorCodes.api","errorCodes.vnext"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.errorCodes.api,base.errorCodes.api),reason:"canonical API error code removed"},
    {pass:setContainsAll(candidate.errorCodes.vnext,base.errorCodes.vnext),reason:"canonical VNext error code removed"}
  ]));
}
export function gate14NumericScopes(base,candidate){
  return wrap(GATE_IDS[13],["numericScopes"],candidate,()=>{
    const checks=[];
    for(const [scope,law] of Object.entries(base.numericScopes)){
      const next=candidate.numericScopes[scope];
      checks.push({pass:!!next,reason:`numeric scope removed: ${scope}`});
      if(!next) continue;
      for(const field of ["format","carrier","overflow","divisionByZero"]){
        checks.push({
          pass:next[field]===law[field],
          reason:`numeric law drift ${scope}.${field}: ${law[field]} -> ${next[field]}`
        });
      }
    }
    return passFail(checks);
  });
}
export function gate15Queue(base,candidate){
  return wrap(GATE_IDS[14],["queue"],candidate,()=>{
    const mustStayTrue=["idempotencyRequired","validateBeforeEnqueue","revalidateBeforeConsume","freezeCancelsPendingRelease","stopCancelsAll"];
    const checks=mustStayTrue.map(k=>({pass:candidate.queue[k]===true,reason:`queue safety weakened: ${k}`}));
    checks.push({pass:candidate.queue.autoRetryDefault===false,reason:"unsafe automatic retry enabled by default"});
    return passFail(checks);
  });
}
export function gate16Vault(base,candidate){
  return wrap(GATE_IDS[15],["vault"],candidate,()=>{
    const keys=["appendOnlyRevisions","overwriteRevisionForbidden","monotonicallyIncreasingRevision","optimisticConcurrency","commitRequiresExistingRevision"];
    return passFail(keys.map(k=>({pass:candidate.vault[k]===true,reason:`Vault lineage weakened: ${k}`})));
  });
}
export function gate17Adapter(base,candidate){
  return wrap(GATE_IDS[16],["adapter"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.adapter.requiredFields,base.adapter.requiredFields),reason:"AgentAdapter required field removed"},
    {pass:setContainsAll(candidate.adapter.requiredMethods,base.adapter.requiredMethods),reason:"AgentAdapter required method removed"}
  ]));
}
export function gate18Evidence(base,candidate){
  return wrap(GATE_IDS[17],["evidence"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.evidence.requiredFields,base.evidence.requiredFields),reason:"evidence field removed"},
    {pass:candidate.evidence.hashHexLength===base.evidence.hashHexLength,reason:"evidence hash width changed"},
    {pass:candidate.evidence.confidenceMinQ64>=base.evidence.confidenceMinQ64,reason:"evidence confidence lower bound weakened"},
    {pass:candidate.evidence.confidenceMaxQ64<=base.evidence.confidenceMaxQ64,reason:"evidence confidence upper bound widened beyond unit interval"}
  ]));
}
export function gate19ObsUiConfig(base,candidate){
  return wrap(GATE_IDS[18],["observability","uiTruth","config"],candidate,()=>passFail([
    {pass:setContainsAll(candidate.observability.requiredTraceFields,base.observability.requiredTraceFields),reason:"trace linkage field removed"},
    {pass:candidate.observability.freezeRequiresPrimaryIncident===true,reason:"freeze no longer requires a primary incident"},
    {pass:candidate.observability.orphanIncidentForbidden===true,reason:"orphan incident became legal"},
    {pass:candidate.uiTruth.mayInventState===false,reason:"UI allowed to invent state"},
    {pass:candidate.uiTruth.mayMaskFreeze===false,reason:"UI allowed to mask FREEZE"},
    {pass:candidate.uiTruth.mayExposeUnreleasedPartial===false,reason:"UI allowed to expose unreleased partial output"},
    {pass:candidate.uiTruth.optimisticBlockingSuccess===false,reason:"UI allowed optimistic success for blocking action"},
    {pass:setContainsAll(candidate.config.immutableAtRuntime,base.config.immutableAtRuntime),reason:"runtime immutable config weakened"},
    {pass:setContainsAll(candidate.config.mutableRequiresVersionAuditRollback,base.config.mutableRequiresVersionAuditRollback),reason:"version/audit/rollback obligation removed"}
  ]));
}

const GATES_1_19=[
  gate01StateUniverse,gate02TraceForwardSimulation,gate03IllegalTransitionNonexpansion,
  gate04EventOwnerNonwidening,gate05GuardStrength,gate06FreezeStopDominance,
  gate07RecoveryAuthority,gate08ReleasePolicy,gate09ReleaseGates,gate10Rbac,
  gate11ModuleBoundary,gate12Envelope,gate13Errors,gate14NumericScopes,
  gate15Queue,gate16Vault,gate17Adapter,gate18Evidence,gate19ObsUiConfig
];

export function evaluateAll(base,candidate){
  const sub=GATES_1_19.map(fn=>fn(base,candidate));
  const failed=sub.filter(r=>r.status==="FAIL");
  const unknown=sub.filter(r=>r.status==="NOT_VERIFIED");
  const passCount=sub.filter(r=>r.status==="PASS").length;
  const coverageQ64=q64RatioOfCounts(passCount,sub.length);
  const verdict=failed.length>0?"REJECT":unknown.length>0?"DEFER":"KEEP_CANDIDATE";
  const composite=Object.freeze({
    id:GATE_IDS[19],
    status:failed.length>0?"FAIL":unknown.length>0?"NOT_VERIFIED":"PASS",
    verdict,
    authority:"NON_AUTHORITATIVE_LO4_PROPOSAL",
    canPromoteCanon:false,
    canMutateCoreState:false,
    canWriteVault:false,
    coverageQ64,
    riskQ64:q64ComplementUnit(coverageQ64),
    failedGateIds:Object.freeze(failed.map(r=>r.id)),
    unverifiedGateIds:Object.freeze(unknown.map(r=>r.id)),
    candidateHash:sha256Canonical(candidate),
    baselineHash:sha256Canonical(base)
  });
  return Object.freeze({gates:Object.freeze([...sub,composite]),composite});
}
export function summarizeDeterministically(report){
  const items=report.gates.map(g=>({
    id:g.id,status:g.status,reasons:sortedUnique(g.reasons??[])
  }));
  return Object.freeze({
    verdict:report.composite.verdict,
    items,
    hash:sha256Canonical(items)
  });
}
