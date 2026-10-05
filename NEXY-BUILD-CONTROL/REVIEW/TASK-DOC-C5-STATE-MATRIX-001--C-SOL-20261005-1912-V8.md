# Independent Review — TASK-DOC-C5-STATE-MATRIX-001

CHAT_ID: C-SOL-20261005-1912-V8
ROLE: Spec Auditor / Reviewer / Red Team
EPOCH_ID: EPOCH-20261005-b35ee1bf-608426cb
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
FINDING_ID: FINDING-DOC-C5-STATE-ORACLE-001
SOURCE_MUTATION: NONE
VERDICT: P0_FINDING_INDEPENDENTLY_CONFIRMED
REPAIR_ELIGIBILITY: BLOCKED_BY_GLOBAL_WORKER_REF_NAMESPACE

## Primary authority

The locked DOCX FINAL VERDICT at raw paragraphs 9834-9845 declares DOC-C as BUILD SPEC and states that build obligation comes from DOC-C only.

Final DOC-C §5.1 raw paragraphs 10354-10367 includes all eleven SystemEvent members:
boot, execute, agents_done, verified, accepted, rejected, timeout, error, recover, fatal, cancel.

Final DOC-C §5.2 raw paragraphs 10368-10452 explicitly declares error->FREEZE only for:
- RUNNING --error--> FREEZE
- VERIFYING --error--> FREEZE

The same matrix declares:
- RUNNING --timeout--> FREEZE
- CONSENSUS --timeout--> FREEZE
- FREEZE --recover--> READY
- FREEZE --fatal--> STOP
- ANY except STOP --fatal--> STOP

Final DOC-C §5.4 raw paragraphs 10470-10485 declares OWNER hard kill for RUNNING / VERIFYING / CONSENSUS -> FREEZE and does not add ANY-state error semantics.

## Exact source facts

packages/core/vnext-state-matrix.ts currently includes undeclared error->FREEZE rows from INIT, READY, CONSENSUS, STABLE, and FREEZE in addition to the two DOC-C rows. Its source comment incorrectly attributes this to final DOC-C §5.4.

tests/contract/state-matrix.test.ts currently requires error->FREEZE from every non-STOP state and therefore encodes a wrong final-DOC-C oracle. The same test incorrectly calls timeout/cancel non-DOC-C compatibility rails even though final DOC-C §5.1 explicitly includes both events.

core-kernel/src/kernel/vnext_matrix.rs implements error->FREEZE only from RUNNING and VERIFYING, matching final DOC-C. Therefore TypeScript and Rust are semantically divergent at the exact integration SHA.

tests/contract/core-kernel-vnext-parity.test.ts derives the expected Rust transition set from the drifting TypeScript table. At the exact source contents inspected, this oracle should expose a TS/Rust transition mismatch if execution infrastructure actually runs it.

packages/api/bootstrap.ts invokes transitionSystemState("error", "CORE") on bootstrap dependency failure outside any proof that current state is RUNNING/VERIFYING. packages/law/freeze.ts is a generic LAW error-transition wrapper; packages/api/auth-failure.ts calls it for auth persistence failures. Removing undeclared error edges therefore requires call-site redesign rather than merely deleting rows.

## Required repair boundaries

- Remove only transition semantics unsupported by final DOC-C; do not import the earlier Execution Pack ANY-error rule.
- Treat timeout and cancel as final DOC-C SystemEvent members.
- Preserve OWNER hard-kill semantics only for RUNNING/VERIFYING/CONSENSUS.
- Preserve fatal->STOP from every non-STOP state.
- Reconcile bootstrap/auth fail-closed behavior without inventing INIT/READY error transitions.
- Reconcile TypeScript/Rust parity and repair tests whose oracle follows the wrong TypeScript table.
- Do not use existing green assumptions as authority over the primary DOC-C.

## Unknown requiring fail-closed design

Final DOC-C does not state a legal INIT/READY error transition. It also requires fail-closed behavior at system level. The exact mechanism for bootstrap/auth dependency failure outside RUNNING/VERIFYING must therefore be derived from other active DOC-C/system-law clauses or kept as a design conflict; it must not be guessed.

## Blocker

INC-BRANCH-NAMESPACE-001 prevents creation of the mandated worker branch NEXY.AI-Test-AI/work/TASK-DOC-C5-STATE-MATRIX-001. Direct integration-branch mutation remains forbidden.

## Closure effect

ACTIONABLE_CODE_GAP: CONFIRMED
PARITY_DEFECT: CONFIRMED
TEST_ORACLE_DEFECT: CONFIRMED
AUTHORITY_VIOLATION: CONFIRMED
GAP_FIXED: NO
REVERIFY_REQUIRED: YES
CODE_CLOSURE_ELIGIBLE: NO
