# Second Independent Review — TASK-DOC-C4-RUN-STATE-BOUNDARY-001

REVIEW_ID: RVW-DOC-C4-RUN-STATE-BOUNDARY-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-DOC-C4-RUN-STATE-BOUNDARY-001
FINDING_ID: FINDING-DOC-C4-RUN-STATE-BOUNDARY-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: INDEPENDENT_BOUNDARY_CONTRACT_REVIEWER / RED_TEAM
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## PRIMARY AUTHORITY
- Final DOC-C raw 9955-9963 defines closed SystemState: INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP.
- Final DOC-C raw 10222-10242 defines GET /api/runs/:id response data.state: SystemState.

## EXACT-HEAD SOURCE FACTS
- prisma/schema.prisma blob 0c557a1bb9b02859bb479655575c3566e201eb6f stores PipelineRun.runState as unconstrained String @db.VarChar(16).
- packages/api/directives.ts blob 8cd214c87e5aa55561e52347802ec8172feadc36 reads that string.
- handleGetRun computes a safe-ish local envelopeState fallback, but then emits data.state = run.runState without validating the persisted value.
- tests/integration/directives/read-auth.spec.ts blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e covers valid states/shape but contains neither BROKEN_STATE nor SystemStateSchema malformed-state coverage.

## COUNTEREXAMPLE
Given an otherwise owned/authorized persisted run with runState="BROKEN_STATE", the current control flow reaches the 200 response and emits data.state="BROKEN_STATE". That value is outside the required final-DOC-C SystemState union.

## VERDICT
BOUNDARY_VALIDATION_DEFECT: CONFIRMED
CANONICAL_RESPONSE_CONTRACT_DRIFT: CONFIRMED
MISSING_REQUIRED_TEST: CONFIRMED
TASK_DESIGN: APPROVED_WITH_FAILURE-MAPPING_GUARD
REVIEW_RESULT: SECOND_INDEPENDENT_CONFIRMATION

## REPAIR CONSTRAINT
Validate the persisted state before any successful canonical serialization and do not coerce malformed state into a valid member. The exact rejection HTTP status/error envelope is not specified by the cited route section; derive it from separate active authority or an established fail-closed boundary before implementation. Do not guess a new error mapping.

GLOBAL_BLOCKER: INC-BRANCH-NAMESPACE-001 prevents Constitution-compliant isolated source/test mutation.
