REVIEW_ID: R-DOC-C5-C-SOL-20261005-1739-V8-002
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
REVIEWER: C-SOL-20261005-1739-V8
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
RESULT: CHANGES_REQUIRED_WITH_REPAIR_CONTRACT_V2
FINAL_CANDIDATE_REVIEW: NO
COUNTS_TOWARD_FINAL_REVIEW_COMPLETED: false
SOURCE_MUTATION: NONE

# Authority facts

1. Final DOC-C 5.1 includes boot, execute, agents_done, verified, accepted, rejected, timeout, error, recover, fatal, cancel.
2. Final DOC-C 5.2 authorizes error -> FREEZE only from RUNNING and VERIFYING.
3. Final DOC-C 5.2 authorizes fatal -> STOP from every non-STOP state.
4. Final DOC-C 5.4 authorizes OWNER hard-kill only from RUNNING / VERIFYING / CONSENSUS -> FREEZE.
5. Final DOC-C 5.6 says every legal transition emits EventLog and FREEZE/STOP transitions create a primary incident.
6. DOC-B final law says unknown is FREEZE or silence and No patch / No guess / No mask. It does not authorize fabrication of a DOC-C transition.
7. Next.js instrumentation register is the existing application startup admission boundary; repository apps/web/instrumentation.ts awaits bootstrap before request handling.

# Confirmed source defects at SOURCE_SHA

A. packages/core/vnext-state-matrix.ts contains five unauthorized error -> FREEZE rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
B. tests/contract/state-matrix.test.ts encodes those unauthorized rows and misclassifies timeout/cancel.
C. packages/api/bootstrap.ts attempts transitionSystemState("error") on pre-admission dependency/tick-floor failure.
D. packages/law/freeze.ts hardcodes the error event for every buildFreezeEnvelope caller and therefore has a wider semantic contract than DOC-C.
E. packages/api/auth-failure.ts uses buildFreezeEnvelope for request-scoped persistence/evidence failures even when canonical state is INIT/READY/STABLE/etc.
F. packages/queue/workers.ts uses buildFreezeEnvelope for a failed job with no run boundary; that call is not guaranteed to occur in RUNNING/VERIFYING global SystemState.
G. tests/integration/freeze-mechanism.spec.ts and tests/integration/freeze-all-causes.spec.ts start at READY and require buildFreezeEnvelope to enter FREEZE, so they are test-oracle defects after final DOC-C.
H. the older proposed process-local runtime FREEZE quarantine is stale. F-C5D62B7F0-DOC-C5-QUARANTINE-RECOVERY proves that transition reconciliation can restore durable READY/INIT after a denied recovery, clearing the stronger runtime-only quarantine.

# Repair contract V2

## 1. Canonical matrix

- Remove unauthorized error rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
- Keep error -> FREEZE only for RUNNING and VERIFYING.
- Keep fatal -> STOP for every non-STOP state.
- Keep final DOC-C timeout/cancel rows exactly.
- Keep Rust/TypeScript semantic parity exact.
- Correct all tests that preserve the historical ANY-error oracle.

## 2. Pre-admission integrity interlock, separate from SystemState

Do NOT model startup/hydration/tick-floor failure by assigning canonical SystemState FREEZE.

Introduce a process-global, non-FSM admission-integrity latch in the system-state/startup boundary, with semantics equivalent to:

- CLOSED initially false / no failure.
- Once a pre-admission integrity failure is observed, latch CLOSED for the remainder of that process.
- Store only redacted/typed failure identity required for deterministic rejection; do not pretend an FSM transition occurred.
- No recover event can clear this latch.
- No durable-state reconciliation can clear this latch.
- Only process restart may clear it, after which normal hydration/tick-floor establishment must succeed again.
- STOP remains untouched and irreversible.
- When CLOSED, transitionSystemState and transitionSystemStateTransactionally must reject before any durable mutation.
- A test-only reset may clear the latch only under NODE_ENV=test.

This is an admission/interlock invariant, not a ninth SystemState and not a SystemEvent.

## 3. Hydration failure

- hydrateSystemState must latch admission CLOSED when durable truth cannot be established.
- It must reject.
- It must not fabricate a durable FREEZE transition, EventLog or incident.
- Prefer not to overwrite the canonical cached state with a synthetic FREEZE value; the failure latch is the authority for non-admission.
- Repeated hydration calls in the same process must continue rejecting while the latch is CLOSED.
- Explicit recover cannot bypass this condition.

## 4. Bootstrap/tick-floor failure

- establish durable state and durable tick floor before INIT -> READY.
- If readMaxPersistedTick / setEpochBase / required hydration fails, latch admission CLOSED and reject bootstrap.
- Never call transitionSystemState("error") from INIT/READY.
- Never call currentTick for durable evidence before the durable floor is established.
- Never emit a fake FSM EventLog/incident.
- A repeated bootstrap in the same process must remain rejected even if the dependency later becomes reachable; restart is required to re-establish truth from a clean process boundary.
- The existing Next.js startup registration must remain awaited, so rejected bootstrap means no request admission in the normal web runtime.

## 5. Auth persistence/evidence failure

Auth dependency/evidence failures are request-level fail-closed errors unless the current canonical state independently has a legal DOC-C transition for the actual event.

Required behavior:
- Reject the request; never continue the auth success path.
- Do not call global error -> FREEZE from INIT/READY/CONSENSUS/STABLE/FREEZE.
- Preserve STOP/FREEZE if already canonical.
- Otherwise return a non-healthy status/envelope using the actual canonical state; do not fabricate state=FREEZE.
- Route-specific HTTP/ErrorCode pairs must be separately reconciled to final DOC-C 4.2. Do not invent a 500/503 pair merely to preserve current code. request-otac explicitly declares 503 DEPENDENCY_FAILURE for email-provider failure; verify-otac/logout matrices do not declare a generic persistence failure pair.
- Mandatory audit failure remains fail-closed even when no authoritative audit row can be written; stderr/operational evidence must not masquerade as canonical AuditLog evidence.

## 6. buildFreezeEnvelope contract

The helper must no longer imply "any cause can globally FREEZE through error".

Acceptable minimal designs:
A. Narrow it to a legal error-transition helper whose precondition is canonical RUNNING or VERIFYING; reject everywhere else before mutation.
B. Replace it with event-explicit terminal transition helpers where the caller supplies an authoritative legal event (error / timeout / rejected / cancel / fatal) and required guards.

Forbidden:
- silently choosing error for every terminal cause;
- direct runtime SystemState assignment;
- broadening the matrix to save old callers/tests.

Every caller must be audited after helper narrowing. Current runtime callers requiring reclassification are auth-failure.ts and queue/workers.ts no-run failure path.

## 7. Queue worker without run boundary

A worker failure with no PipelineRun identity cannot fabricate a run-bound or global error transition.

Required:
- emit non-authoritative operational alarm/log evidence as available;
- fail/withhold work at the worker/service admission boundary;
- only perform a canonical global transition if the current SystemState + explicit authoritative event makes that transition legal;
- do not use buildFreezeEnvelope merely because the error is severe.

The exact worker-process liveness/readiness mechanism is a dependent design item and must be proven before source mutation if helper narrowing would otherwise remove its fail-closed behavior.

# Required tests

1. Exact DOC-C transition-set oracle, including exact error states RUNNING+VERIFYING.
2. Rust/TypeScript parity oracle unchanged in strictness.
3. INIT bootstrap tick-floor failure: latch CLOSED, no transition/event/incident write, bootstrap rejects.
4. READY/repeated bootstrap failure: latch remains CLOSED; no retry admission in same process.
5. Durable hydration failure: latch CLOSED; later recover attempt cannot clear it.
6. VNextStateTransitionDenied reconciliation cannot clear the admission latch.
7. STOP stays STOP and latch cannot move STOP.
8. Auth persistence failure from READY: request rejected; no error FSM transition; no false FREEZE state.
9. Auth persistence failure while already FREEZE/STOP preserves canonical state.
10. buildFreezeEnvelope or replacement rejects unauthorized READY/INIT invocation.
11. Legal RUNNING error and VERIFYING error still create required incident + EventLog/AuditLog evidence.
12. Queue no-run failure cannot manufacture global error transition.
13. Mutation test: reintroducing any extra error row or a recover-latch clear must be killed by tests.

# Scope impact

Direct task scope remains TASK-DOC-C5-STATE-MATRIX-001. Dependent files discovered by caller audit:
- packages/queue/workers.ts
- tests/integration/freeze-mechanism.spec.ts
- tests/integration/freeze-all-causes.spec.ts
- tests/coverage/judge-law.test.ts
- tests/contract/freeze-only-via-builder.spec.ts

These are affected verification/dependency paths, not authority to invent behavior outside DOC-C.

# Remaining blockers

1. SOURCE MUTATION: blocked by GLOBAL-WORKER-BRANCH-PREFIX-REF-NAMESPACE-COLLISION. refs/heads/NEXY.AI-Test-AI prevents creation of refs/heads/NEXY.AI-Test-AI/work/*.
2. AUTH ERROR SURFACE: exact route-specific persistence failure HTTP/ErrorCode behavior is not fully declared for every auth route in final DOC-C and must be reconciled without widening authority.
3. QUEUE NO-RUN AVAILABILITY: fail-closed worker/service mechanism needs explicit proof after removing the invalid universal error-FREEZE helper.
4. EXECUTED TEST EVIDENCE: unavailable for a repaired candidate because no legal worker ref can be created; integration HEAD CI also has documented zero-step runner infrastructure failures.

IMPLEMENTATION_APPROVAL: NO
REASON: Core repair direction is now safe against the stale quarantine recovery bypass, but auth route error-surface and queue no-run availability must be resolved, and the mandated worker branch namespace is Git-invalid.

NEXT_EXACT_STEP:
- Audit final DOC-C route/error authority for auth persistence failures and the queue/service readiness boundary.
- Record any separate requirement gap.
- Once design sub-blockers close, request independent review.
- Source implementation remains prohibited until a Constitution-authorized Git-valid isolated worker mechanism exists.
