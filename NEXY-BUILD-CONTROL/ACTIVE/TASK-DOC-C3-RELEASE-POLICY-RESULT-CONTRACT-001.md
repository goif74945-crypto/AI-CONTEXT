TASK_ID: TASK-DOC-C3-RELEASE-POLICY-RESULT-CONTRACT-001
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING_TEST_ORACLE
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-3-3-RELEASE-POLICY-RESULT
FINDING_ID: FINDING-DOC-C3-RELEASE-POLICY-RESULT-CONTRACT-TEST-GAP-001
SEMANTIC_SCOPE: Complete the existing ReleasePolicyResult contract oracle for required numeric threshold_snapshot fields only.
TARGET_PATHS:
- tests/contract/release-policy-result.test.ts
REQUIRED:
- each of confidence_min, deterministic_match_min, quorum_min, evidence_min is required
- each threshold field rejects non-number values
- preserve existing passing/failing runtime-schema binding and canonical ErrorCode rejection
FORBIDDEN:
- no runtime policy mutation
- no NEXY.ai mutation
BASE_EVIDENCE: current test now exists but does not yet assert missing/wrong-type threshold fields fail schema validation.
