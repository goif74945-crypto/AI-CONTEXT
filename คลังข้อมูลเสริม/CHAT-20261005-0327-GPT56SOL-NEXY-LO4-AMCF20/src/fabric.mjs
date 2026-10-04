import { sha256Canonical, sha256Text } from "./canonical.mjs";
import { Q64Error, Q_ONE, Q_ZERO, qAbs, qAdd, qCmp, qDiv, qFromInt, qFromRatio, qMul, qSerialize, qSub, qUnitRatio } from "./q64.mjs";

const PASS="PASS", FAIL="FAIL", DEFER="DEFER", FREEZE="FREEZE";
const ok=(system,evidence={})=>({system,status:PASS,evidence});
const fail=(system,reason,evidence={})=>({system,status:FAIL,reason,evidence});
const defer=(system,reason,evidence={})=>({system,status:DEFER,reason,evidence});
const freeze=(system,reason,evidence={})=>({system,status:FREEZE,reason,evidence});
function guard(system, fn) { try { return fn(); } catch (e) { return freeze(system, e instanceof Q64Error ? e.code : `INVALID_INPUT:${e?.message??String(e)}`); } }
function reqString(v,name){if(typeof v!=="string"||v.length===0)throw new Error(name);return v;}
function reqStrings(v,name){if(!Array.isArray(v)||v.some(x=>typeof x!=="string"||x.length===0))throw new Error(name);return v;}
function reqBool(v,name){if(typeof v!=="boolean")throw new Error(name);return v;}
function uniqSorted(a){return [...new Set(a)].sort();}

// S01 Provider Capability Fingerprinter
export function s01Fingerprint(adapter){return guard("S01",()=>{
  const shape={id:reqString(adapter.id,"id"),provider:reqString(adapter.provider,"provider"),schema_version:reqString(adapter.schema_version,"schema_version"),supported_modes:uniqSorted(reqStrings(adapter.supported_modes,"supported_modes")),deterministic_capable:reqBool(adapter.deterministic_capable,"deterministic_capable"),critical:reqBool(adapter.critical,"critical"),max_context_raw:reqString(adapter.max_context_raw,"max_context_raw")};
  return ok("S01",{fingerprint:sha256Canonical(shape),shape});
});}

// S02 Adapter Contract Compatibility Gate
export function s02AdapterContract(candidate){return guard("S02",()=>{
  for(const k of ["id","provider","schema_version","max_context_raw"]) reqString(candidate[k],k);
  reqStrings(candidate.supported_modes,"supported_modes"); reqBool(candidate.deterministic_capable,"deterministic_capable"); reqBool(candidate.critical,"critical");
  return ok("S02",{contract:"AgentAdapter-compatible-metadata"});
});}

// S03 Schema Evolution Gate
export function s03SchemaEvolution(baseline,candidate,compatibleSchemas=[]){return guard("S03",()=>{
  const b=reqString(baseline.schema_version,"baseline.schema_version"), c=reqString(candidate.schema_version,"candidate.schema_version");
  if(c===b) return ok("S03",{schema:c});
  if(compatibleSchemas.includes(`${b}->${c}`)) return ok("S03",{schema:c,migration:`${b}->${c}`});
  return defer("S03","SCHEMA_COMPATIBILITY_NOT_PROVEN",{baseline:b,candidate:c});
});}

// S04 Mode Coverage Preservation
export function s04ModeCoverage(baseline,candidate){return guard("S04",()=>{
  const b=uniqSorted(reqStrings(baseline.supported_modes,"baseline.modes")); const c=new Set(reqStrings(candidate.supported_modes,"candidate.modes"));
  const missing=b.filter(x=>!c.has(x)); return missing.length?fail("S04","MODE_COVERAGE_REGRESSION",{missing}):ok("S04",{covered:b});
});}

// S05 Context Capacity Gate (Q64.64 counts)
export function s05ContextCapacity(baseline,candidate){return guard("S05",()=>{
  const b=BigInt(reqString(baseline.max_context_raw,"baseline.max_context_raw")); const c=BigInt(reqString(candidate.max_context_raw,"candidate.max_context_raw"));
  return qCmp(c,b)>=0?ok("S05",{baseline_raw:qSerialize(b),candidate_raw:qSerialize(c)}):fail("S05","CONTEXT_CAPACITY_REGRESSION",{baseline_raw:qSerialize(b),candidate_raw:qSerialize(c)});
});}

// S06 Health Signal Normalizer
export function s06HealthNormalize(signal){return guard("S06",()=>{
  const classification=reqString(signal.classification,"classification");
  if(!["HEALTHY","DEGRADED","UNHEALTHY"].includes(classification)) return freeze("S06","UNKNOWN_HEALTH_CLASS");
  const normalized=classification==="HEALTHY"?"AVAILABLE":classification==="DEGRADED"?"SHADOW_ONLY":"EXCLUDED";
  return ok("S06",{normalized});
});}

// S07 Latency Budget Sentinel, all thresholds Q64.64 raw strings
export function s07LatencyBudget(observedRaw,budgetRaw){return guard("S07",()=>{
  const o=BigInt(reqString(observedRaw,"observedRaw")), b=BigInt(reqString(budgetRaw,"budgetRaw"));
  return qCmp(o,b)<=0?ok("S07",{observed_raw:qSerialize(o),budget_raw:qSerialize(b)}):fail("S07","LATENCY_BUDGET_EXCEEDED",{observed_raw:qSerialize(o),budget_raw:qSerialize(b)});
});}

// S08 Reliability Window Ledger
export function s08Reliability(events){return guard("S08",()=>{
  if(!Array.isArray(events)||events.length===0)throw new Error("events");
  let passed=0n; for(const e of events){if(e==="PASS")passed++;else if(e!=="FAIL")throw new Error("event");}
  const ratio=qUnitRatio(passed,BigInt(events.length)); return ok("S08",{pass_ratio_raw:qSerialize(ratio),passed:passed.toString(),total:String(events.length)});
});}

// S09 Deterministic Degradation Trend Detector
export function s09DegradationTrend(seriesRaw,maxDropRaw){return guard("S09",()=>{
  if(!Array.isArray(seriesRaw)||seriesRaw.length<3) return defer("S09","INSUFFICIENT_WINDOW");
  const s=seriesRaw.map(x=>BigInt(reqString(x,"seriesRaw"))); const maxDrop=BigInt(reqString(maxDropRaw,"maxDropRaw"));
  let worst=0n; let monotonic=true; for(let i=1;i<s.length;i++){const delta=qSub(s[i-1],s[i]); if(qCmp(delta,0n)<0)monotonic=false; if(qCmp(delta,worst)>0)worst=delta;}
  if(monotonic&&qCmp(worst,maxDrop)>0)return fail("S09","DEGRADATION_TREND",{worst_drop_raw:qSerialize(worst)});
  return ok("S09",{worst_drop_raw:qSerialize(worst),monotonic_nonincreasing:monotonic});
});}

// S10 Behavioral Golden Vector Probe
export function s10GoldenVectors(vectors){return guard("S10",()=>{
  if(!Array.isArray(vectors)||vectors.length===0)throw new Error("vectors"); let pass=0n; const mismatches=[];
  for(const v of vectors){const actual=sha256Text(reqString(v.actual,"actual")); const expected=reqString(v.expected_hash,"expected_hash"); if(actual===expected)pass++;else mismatches.push(reqString(v.id,"id"));}
  const ratio=qUnitRatio(pass,BigInt(vectors.length)); return mismatches.length?fail("S10","GOLDEN_VECTOR_MISMATCH",{mismatches,pass_ratio_raw:qSerialize(ratio)}):ok("S10",{pass_ratio_raw:qSerialize(ratio)});
});}

// S11 Determinism Replay Comparator
export function s11Replay(replays){return guard("S11",()=>{
  if(!Array.isArray(replays)||replays.length<2)throw new Error("replays"); const hashes=replays.map(sha256Canonical); const base=hashes[0]; const bad=hashes.map((h,i)=>h===base?null:i).filter(x=>x!==null);
  return bad.length?fail("S11","NON_DETERMINISTIC_REPLAY",{hashes,bad_indexes:bad}):ok("S11",{hash:base,replay_count:String(replays.length)});
});}

// S12 Evidence Contract Preservation
export function s12EvidenceContract(items){return guard("S12",()=>{
  if(!Array.isArray(items)||items.length===0)return defer("S12","NO_EVIDENCE_SAMPLE"); const required=["id","source","source_type","content","hash","confidence_raw","verified","collected_at","normalization_version"];
  const bad=[]; for(let i=0;i<items.length;i++){for(const k of required){if(items[i]?.[k]===undefined)bad.push(`${i}:${k}`);} if(items[i]?.hash!==undefined&&!/^[0-9a-f]{64}$/.test(items[i].hash))bad.push(`${i}:hash_format`); if(items[i]?.confidence_raw!==undefined)BigInt(reqString(items[i].confidence_raw,"confidence_raw"));}
  return bad.length?fail("S12","EVIDENCE_CONTRACT_REGRESSION",{violations:bad}):ok("S12",{sample_count:String(items.length)});
});}

// S13 FREEZE semantics preservation
export function s13FreezeSemantics(cases){return guard("S13",()=>{
  if(!Array.isArray(cases)||cases.length===0)throw new Error("cases"); const violations=[];
  for(const c of cases){if(c.expected==="FREEZE"&&c.actual!=="FREEZE")violations.push(reqString(c.id,"id"));}
  return violations.length?fail("S13","FREEZE_SEMANTICS_REGRESSION",{violations}):ok("S13",{checked:String(cases.length)});
});}

// S14 Quorum Viability Simulator, quorum threshold Q64.64
export function s14QuorumViability(agentStates,requiredQuorumRaw){return guard("S14",()=>{
  if(!Array.isArray(agentStates))throw new Error("agentStates"); const active=BigInt(agentStates.filter(x=>x==="AVAILABLE").length); const activeQ=qFromInt(active); const required=BigInt(reqString(requiredQuorumRaw,"requiredQuorumRaw"));
  return qCmp(activeQ,required)>=0?ok("S14",{active_q64_raw:qSerialize(activeQ),required_q64_raw:qSerialize(required)}):fail("S14","QUORUM_NOT_VIABLE",{active_q64_raw:qSerialize(activeQ),required_q64_raw:qSerialize(required)});
});}

// S15 Correlated-Failure Diversity Guard
export function s15Diversity(adapters,minDistinctProvidersRaw){return guard("S15",()=>{
  if(!Array.isArray(adapters)||adapters.length===0)throw new Error("adapters"); const distinct=BigInt(new Set(adapters.map(a=>reqString(a.provider,"provider"))).size); const dq=qFromInt(distinct); const min=BigInt(reqString(minDistinctProvidersRaw,"minDistinctProvidersRaw"));
  return qCmp(dq,min)>=0?ok("S15",{distinct_q64_raw:qSerialize(dq)}):fail("S15","PROVIDER_DIVERSITY_TOO_LOW",{distinct_q64_raw:qSerialize(dq),required_raw:qSerialize(min)});
});}

// S16 Shadow Routing Evaluator
export function s16ShadowRouting(samples,minPassRatioRaw){return guard("S16",()=>{
  if(!Array.isArray(samples)||samples.length===0)throw new Error("samples"); let pass=0n; const failed=[];
  for(const s of samples){if(s.baseline_hash===s.candidate_hash&&s.evidence_ok===true&&s.freeze_ok===true)pass++;else failed.push(reqString(s.id,"id"));}
  const ratio=qUnitRatio(pass,BigInt(samples.length)); const min=BigInt(reqString(minPassRatioRaw,"minPassRatioRaw"));
  return qCmp(ratio,min)>=0?ok("S16",{pass_ratio_raw:qSerialize(ratio)}):fail("S16","SHADOW_PARITY_BELOW_THRESHOLD",{pass_ratio_raw:qSerialize(ratio),failed});
});}

// S17 Cutover Readiness Gate
export function s17CutoverReadiness(results,pinned,current){return guard("S17",()=>{
  if(!Array.isArray(results)||results.length===0)throw new Error("results"); if(pinned.nexy!==current.nexy||pinned.spec!==current.spec)return defer("S17","PINNED_SOURCE_STALE",{pinned,current});
  const blockers=results.filter(r=>r.status!==PASS).map(r=>`${r.system}:${r.status}`); return blockers.length?defer("S17","GATES_NOT_ALL_PASS",{blockers}):ok("S17",{gate_count:String(results.length)});
});}

// S18 Rollback Capsule Builder
export function s18RollbackCapsule(topology,pins){return guard("S18",()=>{
  if(!Array.isArray(topology)||topology.length===0)throw new Error("topology"); const capsule={schema:"AMCF20-ROLLBACK-1",topology:topology.map(a=>({id:reqString(a.id,"id"),provider:reqString(a.provider,"provider"),fingerprint:reqString(a.fingerprint,"fingerprint")})).sort((a,b)=>a.id.localeCompare(b.id)),pins:{nexy:reqString(pins.nexy,"pins.nexy"),spec:reqString(pins.spec,"pins.spec")}};
  return ok("S18",{capsule,rollback_hash:sha256Canonical(capsule)});
});}

// S19 Post-swap Drift Sentinel
export function s19PostSwapDrift(observed,policy){return guard("S19",()=>{
  const metrics=["reliability_raw","evidence_ratio_raw","shadow_parity_raw"]; const below=[]; for(const m of metrics){const o=BigInt(reqString(observed[m],m));const p=BigInt(reqString(policy[`min_${m}`],`min_${m}`));if(qCmp(o,p)<0)below.push(m);}
  const latency=BigInt(reqString(observed.latency_raw,"latency_raw")); const maxLat=BigInt(reqString(policy.max_latency_raw,"max_latency_raw")); if(qCmp(latency,maxLat)>0)below.push("latency_raw");
  return below.length?fail("S19","POST_SWAP_DRIFT",{violations:below}):ok("S19",{metrics_checked:String(metrics.length+1)});
});}

// S20 Continuity Orchestrator — advisory only, never promotion authority.
export function s20Orchestrate(results){return guard("S20",()=>{
  if(!Array.isArray(results)||results.length<19) return defer("S20","INCOMPLETE_SYSTEM_SET",{count:String(results?.length??0)});
  const failures=results.filter(r=>r.status===FAIL||r.status===FREEZE); if(failures.length)return {system:"S20",status:PASS,verdict:"REJECT_CANDIDATE",reason:"PROVEN_BLOCKER",blockers:failures.map(r=>`${r.system}:${r.reason??r.status}`)};
  const unresolved=results.filter(r=>r.status!==PASS); if(unresolved.length)return {system:"S20",status:PASS,verdict:"DEFER",reason:"EVIDENCE_INCOMPLETE",blockers:unresolved.map(r=>`${r.system}:${r.status}`)};
  return {system:"S20",status:PASS,verdict:"PROMOTION_CANDIDATE",reason:"ALL_REFERENCE_GATES_PASS",authority:"ADVISORY_ONLY_NO_PROMOTION_API"};
});}

export const AMCF_SYSTEMS=Object.freeze([
  "S01 Provider Capability Fingerprinter","S02 Adapter Contract Compatibility Gate","S03 Schema Evolution Gate","S04 Mode Coverage Preservation","S05 Context Capacity Gate","S06 Health Signal Normalizer","S07 Latency Budget Sentinel","S08 Reliability Window Ledger","S09 Degradation Trend Detector","S10 Behavioral Golden Vector Probe","S11 Determinism Replay Comparator","S12 Evidence Contract Preserver","S13 Freeze Semantics Preserver","S14 Quorum Viability Simulator","S15 Correlated-Failure Diversity Guard","S16 Shadow Routing Evaluator","S17 Cutover Readiness Gate","S18 Rollback Capsule Builder","S19 Post-Swap Drift Sentinel","S20 Continuity Orchestrator"
]);
export const VERDICTS=Object.freeze({PASS,FAIL,DEFER,FREEZE});
