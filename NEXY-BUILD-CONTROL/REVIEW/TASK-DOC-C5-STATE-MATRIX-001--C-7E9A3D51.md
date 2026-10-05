TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
REVIEWER_CHAT: C-7E9A3D51
STATUS: REVIEW_FAIL_BASELINE
PRIORITY: P0
RISK: CRITICAL
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SCOPE: independent shadow review + test-oracle review; no source mutation
REVIEWED_AT: 2026-10-05T17:18:45+07:00

FACT — AUTHORITY:
- Locked FINAL VERDICT makes DOC-C the BUILD SPEC and states build obligation comes from DOC-C only.
- Final DOC-C state/event matrix contains timeout and cancel in the SystemEvent set.
- Final DOC-C transition rows authorize error -> FREEZE for RUNNING and VERIFYING. No final row authorizes INIT/READY/CONSENSUS/STABLE/FREEZE error -> FREEZE.
- Final DOC-C authorizes fatal -> STOP for ANY state except STOP.

FACT — SOURCE @ EXACT HEAD:
- packages/core/vnext-state-matrix.ts blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e classifies timeout/cancel as extended compatibility rails and includes five extra error -> FREEZE rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
- core-kernel/src/kernel/vnext_matrix.rs blob 2e5a0a1f9109175ede8884e76bddab2f46c79f77 permits error -> FREEZE only from RUNNING and VERIFYING.
- tests/contract/state-matrix.test.ts blob 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba misclassifies timeout/cancel as non-DOC-C compatibility rails and asserts error -> FREEZE from every non-STOP state.
- tests/contract/core-kernel-vnext-parity.test.ts blob a391b2029fc13c3e38a9037c8adf3f10638f0086 compares Rust transition triples exactly against TypeScript VNEXT_TRANSITIONS.

STATIC COUNTEREXAMPLE:
TypeScript contains INIT|error|FREEZE while Rust does not. The parity test derives its expected triples from TypeScript and compares them with Rust using exact equality. Therefore the current source sets are semantically contradictory at HEAD 608426cb30398b1f3461866f7079d2a435c96b96.

TEST-EVIDENCE CLASSIFICATION:
- GitHub combined status for exact HEAD reports context "NEXY Validation R2 - nexy-validation-branch" = failure.
- GitHub returned no GitHub Actions workflow runs for this SHA through the available commit-workflow query.
- Executed-step evidence for the external validation failure was not obtained in this review. Therefore it is NOT classified as SOURCE_TEST_FAIL here.
- The parity contradiction above is static/reasoned proof, not a substitute for the required executed contract/parity tests after repair.

REVIEW RESULT:
FAIL. Current TypeScript runtime and its contract oracle do not match final DOC-C and do not match the Rust mirror. The existing task acceptance criteria are correct on this point. Repair must remove the five non-authoritative TypeScript error rows, classify timeout/cancel as DOC-C events, correct the state-matrix test oracle, preserve fatal->STOP for all non-STOP states, then execute exact-SHA TS contract + Rust/parity verification.

MUTATION STATUS:
Source mutation remains blocked by INCIDENT-WORKER-REF-PREFIX-COLLISION-001. This review does not authorize direct mutation of NEXY.AI-Test-AI and does not create a duplicate task/finding.
