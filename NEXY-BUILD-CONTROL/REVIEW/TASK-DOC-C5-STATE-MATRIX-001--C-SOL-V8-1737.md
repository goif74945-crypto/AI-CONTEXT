REVIEW_ID: R-DOC-C5-C-SOL-V8-1737-001
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
REVIEWER: C-SOL-V8-1737
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
RESULT: CHANGES_REQUIRED
FINAL_CANDIDATE_REVIEW: NO
COUNTS_TOWARD_FINAL_REVIEW_COMPLETED: false
SOURCE_MUTATION: NONE

AUTHORITY:
- final DOC-C 10353-10367 includes timeout and cancel.
- final DOC-C 10368-10452 permits error -> FREEZE only from RUNNING and VERIFYING.
- fatal -> STOP is legal from any non-STOP state.
- owner hard-kill RUNNING/VERIFYING/CONSENSUS -> FREEZE is explicit.

SOURCE:
- packages/core/vnext-state-matrix.ts adds extra error rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
- tests/contract/state-matrix.test.ts requires those extra rows and mislabels timeout/cancel as compatibility-only. This is a test-oracle defect.
- bootstrap.ts currently relies on an error transition from INIT/READY.
- freeze.ts maps every buildFreezeEnvelope call to the error event.
- auth-failure.ts therefore needs separate expected behavior once the matrix is corrected.

DESIGN BLOCKER:
A runtime-only FREEZE assignment is not sufficient by itself because durable INIT/READY can later cause recovery denial and current transition reconciliation can restore the less-safe durable state. Existing finding F-C5D62B7F0-DOC-C5-QUARANTINE-RECOVERY remains valid.

REQUIRED BEFORE IMPLEMENTATION:
1. Correct canonical matrix and test oracle without invented error rows.
2. Define pre-admission fail-closed handling separately from a normal FSM transition.
3. Do not fabricate transition/event/incident persistence when no legal transition occurred.
4. A denied recovery must not clear a stronger fail-closed condition.
5. Preserve STOP irreversibility.
6. Resolve auth evidence/persistence failure behavior explicitly.
7. Add real-semantics tests for INIT bootstrap failure, repeated READY bootstrap failure, and recovery-denial preservation.
8. Obtain another independent review after the design is resolved.

IMPLEMENTATION_APPROVAL: NO
