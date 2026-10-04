import { Q64_ONE, q64FromRatio } from "./q64.mjs";

const T = (from, event, to, owners, guards = []) => Object.freeze({ from, event, to, owners, guards });

export const NEXY_BASELINE = Object.freeze({
  identity: Object.freeze({
    repo: "goif74945-crypto/NEXY.AI-",
    branch: "NEXY.ai",
    commit: "9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43",
    canonSourceSha256: "b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7",
    status: "READ_ONLY_REFERENCE"
  }),
  states: Object.freeze(["INIT","READY","RUNNING","VERIFYING","CONSENSUS","STABLE","FREEZE","STOP"]),
  transitions: Object.freeze([
    T("INIT","boot","READY",["CORE"],["system_valid","not_in_stop"]),
    T("READY","execute","RUNNING",["CORE"],["directive_valid","not_in_stop"]),
    T("RUNNING","agents_done","VERIFYING",["SWARM"],["results_exist","not_in_stop"]),
    T("VERIFYING","verified","CONSENSUS",["JUDGE"],["evidence_valid","not_in_stop"]),
    T("CONSENSUS","accepted","STABLE",["JUDGE"],["quorum_satisfied","release_policy_passed","not_in_stop"]),
    T("CONSENSUS","rejected","FREEZE",["JUDGE"],["not_in_stop"]),
    T("RUNNING","cancel","FREEZE",["OWNER"],["not_in_stop"]),
    T("VERIFYING","cancel","FREEZE",["OWNER"],["not_in_stop"]),
    T("CONSENSUS","cancel","FREEZE",["OWNER"],["not_in_stop"]),
    T("FREEZE","recover","READY",["OWNER","SYSTEM"],["freeze_recovery_allowed","not_in_stop"]),
    T("RUNNING","timeout","FREEZE",["SYSTEM"],["not_in_stop"]),
    T("CONSENSUS","timeout","FREEZE",["SYSTEM"],["not_in_stop"]),
    ...["INIT","READY","RUNNING","VERIFYING","CONSENSUS","STABLE","FREEZE"].map(s=>T(s,"error","FREEZE",["LAW","CORE","AUTH","VAULT","SWARM","API"],["not_in_stop"])),
    ...["INIT","READY","RUNNING","VERIFYING","CONSENSUS","STABLE","FREEZE"].map(s=>T(s,"fatal","STOP",["LAW","AUTH"],["not_in_stop"]))
  ]),
  freezeRecovery: Object.freeze({
    HASH_DIVERGENCE:Object.freeze({recoverable:false,actors:[]}),
    CONFIDENCE_GUILLOTINE:Object.freeze({recoverable:false,actors:[]}),
    EVIDENCE_SHORTFALL:Object.freeze({recoverable:true,actors:["OWNER","SYSTEM"]}),
    SWARM_FREEZE:Object.freeze({recoverable:true,actors:["OWNER","SYSTEM"]}),
    VAULT_COMMIT_CONFLICT:Object.freeze({recoverable:true,actors:["OWNER","SYSTEM"]}),
    SCHEMA_VIOLATION:Object.freeze({recoverable:false,actors:[]})
  }),
  release: Object.freeze({
    requiredBooleanGates:Object.freeze(["accepted","releaseable","quorum_satisfied","law_pre_release_passed","integrity_hash_present","critical_agent_not_failed"]),
    confidenceMinQ64:q64FromRatio(85n,100n),
    deterministicMatchMinQ64:q64FromRatio(90n,100n),
    quorumMin:2,
    evidenceMin:2
  }),
  rbac: Object.freeze({
    create_directive:Object.freeze(["OWNER","OPERATOR","SYSTEM"]),
    view_directive:Object.freeze(["OWNER","OPERATOR","AUDITOR","SYSTEM"]),
    recover_freeze:Object.freeze(["OWNER","SYSTEM"]),
    commit_vault:Object.freeze(["OWNER","SYSTEM"]),
    view_audit:Object.freeze(["OWNER","AUDITOR","SYSTEM"]),
    manage_roles:Object.freeze(["OWNER"])
  }),
  forbiddenModuleEdges:Object.freeze([
    "UI->LAW","UI->VAULT","UI->CORE","CORE->UI","LAW->UI","JUDGE->UI","SWARM->UI",
    "SWARM->VAULT","JUDGE->CORE","JUDGE->VAULT","VAULT->CORE","AUTH->CORE"
  ]),
  envelope:Object.freeze({
    requiredFields:Object.freeze(["status","state","timestamp","request_id","trace_id","version"]),
    statuses:Object.freeze(["OK","DEGRADED","FREEZE","STOP"]),
    states:Object.freeze(["INIT","READY","RUNNING","VERIFYING","CONSENSUS","STABLE","FREEZE","STOP"])
  }),
  errorCodes:Object.freeze({
    api:Object.freeze([
      "INVALID_DIRECTIVE","EMPTY_INPUT","AMBIGUOUS_INPUT","UNVERIFIED_OUTPUT","CONSENSUS_FAILED",
      "EVIDENCE_MISSING","SCHEMA_VIOLATION","STATE_TRANSITION_DENIED","INVALID_STATE","AUTH_INVALID",
      "AUTH_EXPIRED","UNAUTHORIZED","FORBIDDEN","SESSION_REVOKED","DEVICE_MISMATCH","CSRF_INVALID",
      "OTAC_LOCKED","RATE_LIMIT_EXCEEDED","SECURITY_BREACH_DETECTED","SYSTEM_IN_FREEZE","DEPENDENCY_FAILURE",
      "DEPENDENCY_UNHEALTHY","TIMEOUT","AGENT_TIMEOUT","AGENT_SCHEMA_INVALID","FREEZE_RECOVERY_DENIED",
      "VAULT_COMMIT_CONFLICT","REVISION_NOT_FOUND","RELEASE_POLICY_FAILED"
    ]),
    vnext:Object.freeze([
      "CONSENSUS_FAILED","QUORUM_NOT_MET","HASH_DIVERGENCE","STATE_TRANSITION_DENIED","INVALID_STATE_BYTE",
      "FREEZE_WHILE_RUNNING","VAULT_COMMIT_CONFLICT","OPTIMISTIC_CONCURRENCY_FAULT","WAL_INTEGRITY_FAILURE",
      "AGENT_TIMEOUT","SWARM_FREEZE","TRUST_BELOW_THRESHOLD","ADVERSARIAL_SCORE_EXCEEDED","CONFIDENCE_GUILLOTINE",
      "EVIDENCE_SHORTFALL","INTENT_AMBIGUOUS","LAW_PROOF_MISSING","FREEZE_NOT_RECOVERABLE",
      "RELEASE_DETERMINISM_FAIL","RELEASE_QUORUM_MISSING","RELEASE_LAW_REJECTED","RELEASE_CRITICAL_AGENT_FAIL",
      "SCHEMA_VIOLATION","BINARY_PARSE_FAILURE","MAGIC_MISMATCH","UNAUTHORIZED_ACTOR","DUAL_SIGNATURE_MISSING",
      "SESSION_INVALID","SANDBOX_DEPTH_EXCEEDED","UNIVERSE_ESCAPE_DETECTED","MEMORY_PRESSURE_CRITICAL",
      "PRE_DEATH_SEAL_TRIGGERED"
    ])
  }),
  numericScopes:Object.freeze({
    CORE_L9:Object.freeze({format:"Q64.64",carrier:"SIGNED_I128",overflow:"FREEZE",divisionByZero:"FREEZE"}),
    GAME_G15:Object.freeze({format:"Q64.64",carrier:"SIGNED_I128",overflow:"SATURATE",divisionByZero:"FAIL_CLOSED"})
  }),
  queue:Object.freeze({
    idempotencyRequired:true, validateBeforeEnqueue:true, revalidateBeforeConsume:true,
    autoRetryDefault:false, freezeCancelsPendingRelease:true, stopCancelsAll:true
  }),
  vault:Object.freeze({
    appendOnlyRevisions:true, overwriteRevisionForbidden:true, monotonicallyIncreasingRevision:true,
    optimisticConcurrency:true, commitRequiresExistingRevision:true
  }),
  adapter:Object.freeze({
    requiredFields:Object.freeze(["id","provider","schema_version","supported_modes","deterministic_capable","critical","timeout_ms","max_context"]),
    requiredMethods:Object.freeze(["execute","cancel","healthcheck"])
  }),
  evidence:Object.freeze({
    requiredFields:Object.freeze(["id","source","source_type","content","hash","confidence","verified","collected_at","anchors","normalization_version"]),
    hashHexLength:64, confidenceMinQ64:0n, confidenceMaxQ64:Q64_ONE
  }),
  observability:Object.freeze({
    requiredTraceFields:Object.freeze(["request_id","trace_id"]),
    freezeRequiresPrimaryIncident:true,
    orphanIncidentForbidden:true
  }),
  uiTruth:Object.freeze({
    mayInventState:false, mayMaskFreeze:false, mayExposeUnreleasedPartial:false, optimisticBlockingSuccess:false
  }),
  config:Object.freeze({
    immutableAtRuntime:Object.freeze(["schema_version","dependency_rules","state_machine_definition"]),
    mutableRequiresVersionAuditRollback:Object.freeze(["thresholds","agent_enablement","timeouts","quorum","auth_limits"])
  }),
  provenance:Object.freeze({
    "packages/contracts/state.ts":"04efcc7161c5415922e11e16174013d1d4ea40a3",
    "packages/core/vnext-state-matrix.ts":"27e1281fba330784cc3bf2c30e9e1e82f951479b",
    "core-kernel/src/kernel/vnext_matrix.rs":"c55e13839f2bed01a29749f226edef82d1929a4a",
    "packages/contracts/envelope.ts":"daf1156b3431150e667b5e18727d8abe9bdc9b75",
    "packages/swarm/adapters/types.ts":"30e5129a0b8ec2674f75ff3056ea0bf848814c82",
    "core-kernel/src/engine/fixed128_math.rs":"LOCKED_COMMIT_READ_VERIFIED",
    "tests/contract/module-boundaries.test.ts":"b5db76d5ce6621c51f9216b52636b20e660a1956",
    "tests/contract/fixed128-overflow-scope-law.test.ts":"83ff7cbe53988c4fb49f2ff2f251928955cf1abb",
    "packages/contracts/evidence.ts":"6b50f4cf9c0ca7e4c056fc546976e6e5a52d5895",
    "packages/contracts/errors.ts":"b6a1737688399cf0571236f23c0b5ce0f7de5847",
    "packages/queue/payload.ts":"f46513b1123d2a4bef277c6ce08a72656e5d9306",
    "packages/queue/jobs.ts":"e90ac64acc446c5bbd24a710e0208fc76bce9089",
    "packages/queue/run-state.ts":"e162efc8b2a45014bcefbd60dc67a95d8a1e1003",
    "vault/repository.ts":"197698c5514da02af251640aa51ad80597710c8f",
    "packages/phase-f/sovereign/versioning-law.ts":"d0ddd66611868289571263b10cd32a77ce0703da"
  })
});

export function cloneBaseline() { return structuredClone(NEXY_BASELINE); }
