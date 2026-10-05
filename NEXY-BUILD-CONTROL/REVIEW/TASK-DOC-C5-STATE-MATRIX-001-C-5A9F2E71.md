REVIEW_ID: RV-STATE-001-C-5A9F2E71
CHAT_ID: C-5A9F2E71
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
PHASE: DESIGN_ORACLE
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
FINAL_CANDIDATE_REVIEW: PENDING
COUNTS_TOWARD_FINAL_REVIEW_COMPLETED: false

FACT:
- FINAL DOC-C SystemEvent has 11 members: boot, execute, agents_done, verified, accepted, rejected, timeout, error, recover, fatal, cancel.
- FINAL DOC-C permits error->FREEZE for RUNNING and VERIFYING only.
- FINAL DOC-C permits fatal->STOP from every non-STOP state.
- FINAL DOC-C owner cancel maps RUNNING, VERIFYING, CONSENSUS to FREEZE.
- Earlier ANY-except-STOP error->FREEZE text is historical under FINAL VERDICT temporal authority.

BASELINE:
- TS blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e has five extra error rows: INIT, READY, CONSENSUS, STABLE, FREEZE.
- Rust blob 2e5a0a1f9109175ede8884e76bddab2f46c79f77 matches the final DOC-C error rows.
- State test blob 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba encodes the historical error oracle and mislabels timeout/cancel.
- Parity test blob a391b2029fc13c3e38a9037c8adf3f10638f0086 compares exact Rust/TS transition triples.
- check-doc-c blob 5d60b3b8bcce8d11988fd971679eb9685177cc43 proves event membership, not transition completeness.

PATCH_RULES:
- Remove only the five extra TS error rows.
- Keep RUNNING/error/FREEZE and VERIFYING/error/FREEZE.
- Treat timeout/cancel as final DOC-C events.
- Keep Rust transition semantics unchanged unless new primary evidence requires otherwise.
- Correct tests to final DOC-C, never to current buggy runtime.

ADVERSARIAL_CASES:
- error denied from INIT, READY, CONSENSUS, STABLE, FREEZE, STOP.
- error accepted from RUNNING and VERIFYING.
- timeout accepted from RUNNING and CONSENSUS; denied from READY.
- cancel accepted for OWNER from RUNNING, VERIFYING, CONSENSUS; denied elsewhere.
- fatal accepted to STOP from each non-STOP state; STOP has no outgoing transition.
- exact event set is 11 and Rust/TS transition triples are equal.

REQUIRED_EXECUTION:
- npm test -- tests/contract/state-matrix.test.ts tests/contract/core-kernel-vnext-parity.test.ts
- npm run check:doc-c
- affected core-kernel Rust test target used by repository CI
- record exact commit SHA, tree SHA, SPEC_HASH, runner, command, result, exit code.

RESULT: BASELINE_FAIL; PATCH_PLAN_APPROVED_WITH_TEST_ADDITIONS; FINAL_REVIEW_NOT_RUN
BLOCKER: INCIDENT-WORKER-REF-PREFIX-COLLISION-001
