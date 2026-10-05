RESULT_ID: R-DOC-C5-STATE-CANDIDATE-MAP-C-6B8D31F5
TYPE: CANDIDATE_REPAIR_MAP
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
BASE_INTEGRATION_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_MUTATION: NONE
STATUS: READY_FOR_WRITER_AFTER_NAMESPACE_UNBLOCK

AUTHORITY:
- FINAL VERDICT -> DOC-C is sole build obligation.
- Final DOC-C SystemEvent includes timeout and cancel.
- error->FREEZE is legal only from RUNNING and VERIFYING.
- fatal->STOP is legal from every non-STOP state.
- owner hard kill RUNNING/VERIFYING/CONSENSUS -> FREEZE maps to cancel.
- STOP has no outgoing transitions.

ATOMIC SOURCE DELTA:
1. packages/core/vnext-state-matrix.ts
   - Remove exactly five transition triples:
     * INIT|error|FREEZE
     * READY|error|FREEZE
     * CONSENSUS|error|FREEZE
     * STABLE|error|FREEZE
     * FREEZE|error|FREEZE
   - Keep RUNNING|error|FREEZE and VERIFYING|error|FREEZE.
   - Keep fatal->STOP for INIT/READY/RUNNING/VERIFYING/CONSENSUS/STABLE/FREEZE.
   - Keep timeout from RUNNING and CONSENSUS to FREEZE.
   - Keep cancel from RUNNING/VERIFYING/CONSENSUS to FREEZE.
   - Correct comments that currently call timeout/cancel non-DOC-C compatibility rails.
   - Correct comment that currently labels broad error behavior as final DOC-C.
   - Correct comment that implies final DOC-C only requires FREEZE|fatal|STOP; final DOC-C requires ANY-except-STOP fatal->STOP.

2. tests/contract/state-matrix.test.ts
   - Treat timeout and cancel as final DOC-C SystemEvent members, not VNEXT-only extensions.
   - Replace DOC_C_ERROR_STATES seven-state oracle with [RUNNING, VERIFYING].
   - Add/retain negative assertions that INIT/READY/CONSENSUS/STABLE/FREEZE do NOT accept error.
   - Keep timeout/cancel/fatal/recover/STOP-terminal assertions aligned with final DOC-C.

3. tests/contract/core-kernel-vnext-parity.test.ts
   - No expected semantic widening. Existing parity test should pass once TS returns to the 21-triple Rust relation.
   - Re-run after source repair; do not edit merely to force green.

EXPECTED_POST_REPAIR:
- TS transition count = 21.
- Rust transition count = 21.
- TS-only transition set = empty.
- Rust-only transition set = empty.
- Wrong broad-error contract oracle removed.
- Requirement remains TESTING until executed exact-SHA evidence exists.

FORBIDDEN:
- Do not weaken fail-closed consumers simply to satisfy the narrowed matrix.
- Do not invent replacement INIT/READY error transitions.
- Handle DOC-B fail-closed bootstrap/dependency semantics as a separate requirement/design boundary.
