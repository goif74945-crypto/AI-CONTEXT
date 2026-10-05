# Independent Authority / Design Review — T-B05F7A31

REVIEWER_CHAT: C-V8-SOL-BOOT-1912
TASK_ID: T-B05F7A31
STATUS: CHANGES_REQUIRED_DESIGN_CONFIRMED
ROLE: SPEC_AUDITOR / REVIEWER / RED_TEAM
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
INTEGRATION_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
INTEGRATION_TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SOURCE_MUTATION: NONE
PROTECTED_UPSTREAM_MUTATION: NONE

## Authority correction

Direct inspection of the locked DOCX establishes:
- P9834 FINAL VERDICT.
- P9839 DOC-C = BUILD SPEC.
- P9844 Build obligation comes from DOC-C only.
- P9846 begins "1) DOC-B — SYSTEM LAW CANON".
- P9875-P9885 "1.5 Freeze Law" therefore belongs to DOC-B, not DOC-C.
- P9886 begins "2) DOC-C — vNEXT BUILD SPEC".
- Final DOC-C §5.2 P10368-P10452 authorizes error -> FREEZE only from RUNNING and VERIFYING.
- The only ANY-except-STOP terminal row is fatal -> STOP at P10447-P10452.
- Final DOC-C §5.6 P10496-P10499 says every legal transition emits EventLog and transitions to FREEZE/STOP create a primary incident.

Therefore the task record phrase "Final DOC-C §1.5 Freeze Law" is an authority citation error. DOC-B Freeze Law may constrain system design, but it cannot by itself create a DOC-C build transition.

## Exact-head source facts

At NEXY.AI-Test-AI@608426cb30398b1f3461866f7079d2a435c96b96:
- packages/core/vnext-state-matrix.ts blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e still contains five non-final error->FREEZE rows beyond RUNNING/VERIFYING.
- packages/api/bootstrap.ts blob d6292374efca4b55bb3865e7151175674ad06b3e catches tick/admission failure and attempts transitionSystemState("error","CORE",...) while current state may be INIT.
- packages/orch-core/system-state.ts blob 1883414a3d8b2034d06ef30e039b537319e2e0f1 preflights every normal transition against vnextTransition before durable persistence.
- tests/coverage/bootstrap-control-plane.test.ts blob ccd29f3b31248e1e3e9ba48deae529965f0ebbb0 explicitly expects the bootstrap failure path to invoke the CORE error transition.
- tests/contract/hydration-fail-closed.test.ts blob 3b71d4647edc1b452539527767245f48e4917cfb expects a tick-ledger read failure to leave currentSystemState() == FREEZE.
- tests/contract/system-state-persistence.test.ts blob 80edaaf8dccc40bba83d484decac5f31e64d4e7d includes READY + error test setup at lines 179-217; after final matrix correction those incident/persistence tests need a legal RUNNING + error setup instead.
- apps/web/instrumentation.ts blob 51c9ac4edddf3e9d978d35159c84c126b16df965 awaits bootstrap() before request handling; a rejected bootstrap is already a process-admission failure.

## Confirmed defect coupling

1. STATE AUTHORITY: once the TypeScript matrix is corrected to Final DOC-C, INIT + error is illegal. The current bootstrap catch can no longer rely on that transition.
2. TICK INTEGRITY: if readMaxPersistedTick() fails before setEpochBase(), a durable error transition must not be attempted because currentTick() may be below an already persisted ledger tick. This matches existing finding F-B07C4A91-BOOTSTRAP-TICK-REGRESSION.
3. TEST ORACLE: bootstrap-control-plane currently asserts the non-authoritative transition and must change together with the repair.
4. CONTROL AUTHORITY: T-D4A71C2E's current task text still says Final DOC-C §5.4 requires error->FREEZE from every non-STOP state. That is contradicted by the locked final DOC-C and existing P0 finding F-3F7A9D26-01.

## Safe repair contract

FACT:
- Startup must not admit request handling when bootstrap() rejects.
- No durable FSM/EventLog/incident write is safe before the persisted tick floor has been established.
- No INIT/READY/CONSENSUS/STABLE/FREEZE + error edge may be restored merely to preserve old tests.

ENGINEERING INFERENCE:
- Preferred pre-admission failure mechanism is a narrowly-scoped process-local admission quarantine latch that is separate from the canonical FSM state and causes bootstrap/service admission to reject.
- Do not automatically implement quarantine as runtimeState.state = FREEZE; that would look like a canonical state change outside the Final DOC-C transition/log law unless separate authority proves it valid.
- Preserve STOP exactly; quarantine must never downgrade or recover STOP.
- Existing hydrateSystemState() direct runtime FREEZE behavior is not sufficient authority to generalize this pattern and should be independently reviewed rather than treated as precedent.

TEST ORACLE CHANGES REQUIRED:
- bootstrap tick-floor failure: bootstrap rejects; no transitionSystemState("error",...) call; no durable transition/audit/event write; admission quarantine is asserted.
- bootstrap clean path: INIT --boot/CORE--> READY remains unchanged.
- incident/persistence tests that test terminal evidence rather than READY legality should enter RUNNING and use legal RUNNING + error -> FREEZE.
- negative regression: INIT + error remains denied after the matrix repair.
- verify no stale DOC-C §18 / "Final DOC-C §1.5" citation is used as transition authority.

## Blockers

- INC-BRANCH-NAMESPACE-001: mandated worker prefix NEXY.AI-Test-AI/work/ cannot coexist with branch NEXY.AI-Test-AI in Git ref namespace.
- T-D4A71C2E must reconcile its stale authority oracle before bootstrap verification can be trusted.

VERDICT:
CHANGES_REQUIRED / SOURCE_MUTATION_BLOCKED.
This review does not claim executable PASS or project closure.
