# Independent Review 2 — final DOC-C §5 State/Event Matrix

REVIEW_ID: RV-DOC-C5-C-V8-SOL-20261005-1738-B35E
CHAT_ID: C-V8-SOL-20261005-1738-B35E
ROLE: INDEPENDENT_REVIEWER_2 / PARITY_REVIEWER
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
RISK: CRITICAL
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
RESULT: FAIL_CONFIRMED

PRIMARY SPEC FACTS:
- final DOC-C §5.1 declares 11 events including timeout, error, fatal, cancel.
- §5.2 permits error -> FREEZE only for RUNNING and VERIFYING.
- §5.2 + §5.4 permit timeout/cancel rows explicitly described by the matrix/owner actions.
- fatal -> STOP applies to ANY except STOP.
- STOP rejects all events.

SOURCE FACTS:
- packages/orch-core/state-machine.ts blob c412111b4033261c9773f8d7aff55e9fc0ceab22 directly re-exports the implementation from packages/core/vnext-state-matrix.ts, so this is authoritative runtime code rather than an unused compatibility copy.
- packages/core/vnext-state-matrix.ts blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e permits error -> FREEZE from INIT, READY, CONSENSUS, STABLE and FREEZE in addition to the two final-DOC-C rows.
- The TypeScript comment claiming final DOC-C requires error to freeze every lifecycle state except STOP is false under the locked final DOC-C matrix.
- core-kernel/src/kernel/vnext_matrix.rs at the same SOURCE_SHA rejects error outside RUNNING/VERIFYING and therefore disagrees semantically with TypeScript.
- Existing Rust tests explicitly assert error is illegal from INIT, READY, CONSENSUS, STABLE and FREEZE.
- Because system-state imports the re-exported TypeScript transition function, the TypeScript over-permission can affect real state mutation.

CLASSIFICATION:
- SPEC_MISMATCH
- AUTHORITY_VIOLATION
- PARITY_DEFECT
- TEST_ORACLE_DEFECT / documentation drift already identified by reviewer 1

BOOTSTRAP CHALLENGE:
The existing broader TypeScript error matrix cannot be retained merely to make INIT/READY dependency failures enter FREEZE. A fail-safe quarantine path may be required, but it must not be represented as a normal legal DOC-C transition that does not exist.

REQUIRED REPAIR:
- Remove unauthorized error rows from TypeScript.
- Keep RUNNING/VERIFYING error -> FREEZE.
- Keep all final DOC-C fatal/cancel/timeout semantics.
- Make bootstrap/dependency fail-closed behavior explicit outside the legal lifecycle transition table if needed.
- Correct tests/parity oracle to final DOC-C rather than TypeScript implementation.
- Execute exact-SHA TypeScript tests, Rust tests, cross-runtime parity tests, bootstrap failure tests, persistence/recovery tests and red-team counterexamples.

REVIEW SATURATION:
This independently satisfies the task's second static reviewer requirement at current SOURCE_SHA. It does NOT close the task because no repaired candidate or exact-candidate executed evidence exists.

MUTATION:
None. Source mutation remains blocked by INC-BRANCH-NAMESPACE-001.
