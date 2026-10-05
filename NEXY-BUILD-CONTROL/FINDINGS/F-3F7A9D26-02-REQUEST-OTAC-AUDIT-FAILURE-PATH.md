FINDING_ID: F-3F7A9D26-02
FROM_CHAT: C-3F7A9D26
TO_CHAT: C-8E4C12A7
TASK_ID: T-8A3C1D72
HEAD_SHA: a24ab3b9254d300e31de1cdf78aec871fafab96f
SOURCE_COMMIT: 64b86d0a76033feaf092faa59a4a984f8ed0c50d
TEST_COMMIT: a24ab3b9254d300e31de1cdf78aec871fafab96f
SEVERITY: P1
TYPE: INVALID_ERROR_PATH / CONTRACT_DRIFT / MISSING_REQUIRED_TEST
STATUS: OPEN

OBSERVED:
The new request-OTAC admission-audit path correctly attempts AUTH_OTAC_REQUESTED + AuditLog persistence for runtime-config failure, Redis fail-closed rejection, and 429 rejection. However, when that audit transaction itself fails, auditRequestOtacAdmissionFailure() catches the failure, writes a "[FREEZE]" stderr line, and respondRequestOtacAuditUnavailable() returns HTTP 503 with status DEGRADED/currentSystemState().

VERIFIED_SOURCE_CONTRACT:
- packages/api/auth-failure.ts defines respondAuthPersistenceFailure() as the shared auth persistence/audit failure boundary.
- That boundary calls buildFreezeEnvelope(), which delegates to transitionSystemState("error", "LAW", ...) and creates the canonical FREEZE incident path.
- Existing request-OTAC route failures of dualLog() call respondAuthPersistenceFailure().
- packages/law/freeze.ts documents buildFreezeEnvelope() as the centralized FREEZE transition boundary.
- The new middleware helper does not call that boundary and can therefore emit a "[FREEZE]" line while leaving system state non-FREEZE and without the canonical primary incident.

SPEC_RELEVANCE:
FINAL DOC-C §4.2 requires AUTH_OTAC_REQUESTED on request-OTAC success/failure. FINAL DOC-C §5.6 requires legal transitions to emit EventLog and FREEZE/STOP transitions to create the primary incident. The current error path claims FREEZE in stderr without performing the canonical transition.

TEST_GAP:
tests/integration/auth/rate-limit-abuse.spec.ts covers successful persistence for Redis fail-closed rejection and 429 rejection, but does not force event/audit persistence failure. It also does not cover the runtime-config-unavailable audit reason introduced by the source patch.

EXPECTED:
Admission-audit persistence failure must route through the canonical auth persistence/freeze boundary (or a verified equivalent with identical state/incident semantics), and regression tests must prove the failure behavior rather than only successful audit writes.

REPRODUCTION:
At commit a24ab3b9254d300e31de1cdf78aec871fafab96f, make tx.eventLog.create(), tx.auditLog.create(), $queryRaw, or computeAuditChain reject while runtimeProfile=request_otac. Observe auditRequestOtacAdmissionFailure() return false and respondRequestOtacAuditUnavailable() emit DEGRADED without invoking buildFreezeEnvelope()/transitionSystemState().

SOURCE_MUTATION_BY_REVIEWER: NONE
