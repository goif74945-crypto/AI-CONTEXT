# Candidate Shadow Review — Request-OTAC Admission Audit Failure

CHAT_ID: C-3B5E71A2
TASK_ID: T-8A3C1D72
FINDING_ID: F-3F7A9D26-02
REVIEW_TARGET_SHA: a24ab3b9254d300e31de1cdf78aec871fafab96f
INTEGRATION_SHA_AT_REVIEW: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
RATE_LIMIT_BLOB: 7dde2208748d4ae313a515e31bb7f3289b11811a
AUTH_FAILURE_BLOB: 92c3f4c7cebc495d9c8badc1cec0b14b4c71dd0c
FREEZE_BLOB: e2e62e29553b9c62b6de5aef5082c68fe54d478
RATE_LIMIT_TEST_BLOB: 00765200d5bcfcdb062d9e654e9f0cbe3dcfd394
ROLE: SHADOW_REVIEWER
VERDICT: FINDING_CONFIRMED_ON_CANDIDATE
INTEGRATION_IMPACT: NOT_YET_INTEGRATED

## Exact candidate control flow

- request_otac admission failures attempt mandatory AUTH_OTAC_REQUESTED EventLog and rejected AuditLog evidence.
- auditRequestOtacAdmissionFailure() catches any audit transaction failure, prints a [FREEZE] stderr line, and returns false.
- respondRequestOtacAuditUnavailable() then returns HTTP 503 with status DEGRADED/currentSystemState().
- That path does not call respondAuthPersistenceFailure(), buildFreezeEnvelope(), or transitionSystemState().
- Other request-OTAC mandatory audit/persistence failures in packages/api/auth.ts use respondAuthPersistenceFailure().
- respondAuthPersistenceFailure() is the existing centralized auth failure boundary and invokes buildFreezeEnvelope() before responding.
- buildFreezeEnvelope() performs the authoritative persisted/runtime FREEZE transition and primary incident semantics.

## Test gap

The candidate test suite proves successful rejection-audit writes for Redis fail-closed and 429, but does not force:
- runtime config unavailable admission audit
- EventLog create failure
- AuditLog create failure
- sequence allocation failure
- computeAuditChain failure
and therefore does not prove canonical FREEZE behavior when mandatory evidence cannot be persisted.

## Repair direction

Route auditRequestOtacAdmissionFailure() failure through the same verified auth persistence/freeze boundary, or prove an equivalent boundary with identical state/incident semantics. Do not merely change the response label to FREEZE; state transition + primary incident evidence are the authority.

Required regression evidence:
- each mandatory audit dependency failure blocks next()
- canonical freeze transition boundary is invoked
- response reflects resulting authoritative state
- no false 429/503 success semantics after audit persistence failure
- no duplicate primary incident is created

SOURCE_MUTATION_BY_REVIEWER: NONE
UPSTREAM_MUTATION: NONE
NOTE: This is candidate evidence only and must not be counted as integrated Test-AI closure evidence until the repaired candidate is integrated and reverified at the exact integration SHA.
