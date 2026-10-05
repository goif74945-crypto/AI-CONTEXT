# Independent Review — DOC-C §5 State/Event Matrix

REVIEW_ID: RV-DOC-C5-C-5A1712D6
CHAT_ID: C-5A1712D6
ROLE: INDEPENDENT_REVIEWER_1
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
RISK: CRITICAL
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
RESULT: FAIL

FACTS:
1. Final DOC-C §5.1 includes all 11 events: boot, execute, agents_done, verified, accepted, rejected, timeout, error, recover, fatal, cancel.
2. Final DOC-C §5.2 lists error -> FREEZE only for RUNNING and VERIFYING.
3. Final DOC-C §5.2 requires fatal -> STOP for every state except STOP.
4. Final DOC-C §5.4 owner hard-kill authorizes RUNNING / VERIFYING / CONSENSUS -> FREEZE, supporting cancel as a DOC-C owner action.
5. TypeScript at SOURCE_SHA additionally permits error -> FREEZE from INIT, READY, CONSENSUS, STABLE, and FREEZE. These five rows are not authorized by final DOC-C.
6. tests/contract/state-matrix.test.ts wrongly classifies timeout/cancel as non-DOC-C compatibility rails and requires error -> FREEZE from every non-STOP state.
7. Rust core-kernel/src/kernel/vnext_matrix.rs at the same SHA already implements error -> FREEZE only from RUNNING and VERIFYING and exposes all 11 event identities.
8. The parity test derives expected Rust transitions from TypeScript VNEXT_TRANSITIONS, so the incorrect TypeScript oracle pulls the correct Rust matrix toward wrong behavior.

CLASSIFICATION:
- runtime defect: TypeScript state matrix
- wrong test oracle: state-matrix contract test
- parity defect: TypeScript vs Rust
- documentation drift: TypeScript comments

REQUIRED_REPAIR:
- remove unauthorized TypeScript error transitions for INIT, READY, CONSENSUS, STABLE, FREEZE
- retain RUNNING / VERIFYING error -> FREEZE
- retain fatal -> STOP for every non-STOP state
- classify timeout/cancel as DOC-C events
- preserve owner hard-kill cancel semantics for RUNNING / VERIFYING / CONSENSUS
- correct contract/parity oracles from final DOC-C
- run focused state-matrix contract, TS/Rust parity, and affected CORE regression tests on exact candidate SHA

REVIEW_SATURATION:
- satisfies INDEPENDENT_REVIEWER_1
- CRITICAL scope still requires INDEPENDENT_REVIEWER_2 and executed exact-SHA evidence after repair

CONTROL_PLANE_NOTE:
C-5A1712D6 independently reproduced GitHub HTTP 422 for the mandated worker branch prefix at SOURCE_SHA, corroborating INC-BRANCH-NAMESPACE-001. No duplicate incident/broadcast created.


BOOTSTRAP ROOT-CAUSE EXTENSION:
FACT:
- packages/api/bootstrap.ts at 608426cb30398b1f3461866f7079d2a435c96b96 handles a persisted-tick dependency failure by calling transitionSystemState("error", "CORE", ...).
- With the final DOC-C matrix, INIT + error is illegal. transitionSystemState preflight therefore throws VNextStateTransitionDeniedError before any persistence path can force FREEZE.
- bootstrap() catches and suppresses that nested transition error, then throws BOOTSTRAP_FAILED_FREEZE. The runtime state can therefore remain INIT even though the exception text claims FREEZE.
- tests/coverage/bootstrap-control-plane.test.ts mocks transitionSystemState and only asserts that "error" was requested; it does not execute the real state-machine semantics or assert actual runtime FREEZE.
- Commit 27af7f93893c7589e516c269fae41aa467c2cdb9 previously reduced the TypeScript matrix to the final DOC-C error rows but left bootstrap.ts/system-state.ts unchanged, so matrix parity alone did not repair bootstrap fail-closed behavior.
- Commit 51e39a4b110736992d58c01550b57de653539610 broadened TypeScript error transitions to every non-STOP state, which restored a bootstrap path at the cost of violating the later final-verdict DOC-C matrix.

ENGINEERING INFERENCE / REPAIR BOUNDARY:
- Bootstrap dependency quarantine must not be represented by inventing a legal lifecycle error transition from INIT.
- The least-semantic-change repair is a dedicated fail-safe quarantine boundary in system-state, analogous to the existing direct in-memory FREEZE used on hydration/persistence integrity failure: force runtime state to FREEZE without adding an unauthorized VNEXT_TRANSITIONS row, preserve STOP/FREEZE if already terminal, and throw the bootstrap failure.
- Any durable incident/evidence behavior for this non-lifecycle quarantine must be implemented only where storage is available; a dependency outage must not prevent the in-memory fail-safe FREEZE.
- Do not call such a quarantine a normal DOC-C transition and do not emit a fabricated FSM_TRANSITION row for an event that is illegal from INIT.

REQUIRED ACCEPTANCE TEST EXTENSION:
- run bootstrap with the real state-machine/system-state semantics (do not mock the transition oracle) from INIT
- force readMaxPersistedTick/database failure
- assert bootstrap rejects
- assert currentSystemState() === FREEZE
- assert INIT + error remains illegal in the canonical matrix
- assert no fake legal INIT + error transition is introduced
- retain separate persistence/hydration failure tests
