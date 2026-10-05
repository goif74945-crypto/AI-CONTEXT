# Test Evidence: T-D4A71C2E / C-D1CB1B5B

TEST_ID: TEST-DOC-C5-EXACT-BLOB-C-D1CB1B5B
REQ_ID: REQ-DOC-C-STATE-MATRIX-ERROR-001
TASK_ID: T-D4A71C2E
TEST_LEVELS: CONTRACT, PARITY, NEGATIVE, TEST_ORACLE_AUDIT
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
COMMIT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
RUNNER: ChatGPT exact GitHub-blob parser
COMMAND: Parse exact fetched TypeScript/Rust transition triples, compare against locked DOC-C §5.2 + explicit §5.4 owner hard-kill mapping, and inspect contract/parity oracle construction.
RESULT: FAIL
EXIT_CODE: 1

RESULT_DETAILS:
- CANONICAL_TRANSITIONS: 21
- TYPESCRIPT_TRANSITIONS: 26
- RUST_TRANSITIONS: 21
- TYPESCRIPT_EXTRA: 5
- TYPESCRIPT_MISSING: 0
- RUST_EXTRA: 0
- RUST_MISSING: 0
- CONTRACT_TEST_FINAL_EVENT_OMISSIONS: timeout, cancel
- PARITY_ORACLE_DERIVED_FROM_TYPESCRIPT: true

FAILED_ASSERTIONS:
1. TypeScript executable transition set must equal locked final DOC-C semantics.
2. Contract test must classify timeout and cancel as final DOC-C events.
3. Cross-language parity evidence must not be treated as Spec compliance when its expected set is derived from one implementation.

EVIDENCE_BLOBS:
- TS matrix a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e
- Rust matrix 2e5a0a1f9109175ede8884e76bddab2f46c79f77
- contract test 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba
- parity test a391b2029fc13c3e38a9037c8adf3f10638f0086

NOTE:
This is not a full Vitest/Cargo/CI run. It is executed exact-blob contract/parity analysis and must not be represented as whole-repository test evidence.
