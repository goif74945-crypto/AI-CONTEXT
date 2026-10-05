TASK_ID: T-HG-NICKNAME-DIGEST-3E9A41C7
PARENT_TASK: T-6F4B2D10
OWNER_CHAT: C-SOL-20261006-0142-HUMAN-GRAVITY
STATUS: SUSPENDED_TEST_EXECUTION
MUTATION_LEASE: packages/human/dialog-sandbox.ts; tests/integration/dialog-sandbox.spec.ts
SEMANTIC_SCOPE: Prevent presentation-only nickname metadata from changing CORE TASK handoff digest
SOURCE_REPO: goif74945-crypto/NEXY.AI-
BASE_BRANCH: NEXY.AI-Test-AI
BASE_SHA_AT_DISCOVERY: 0828481b36b6f252146b07ace40dd4cd0d759ad4
WORKER_BRANCH: NEXY.AI-Test-AI-work-dialog-friend-guard-7a41c2e9
REQUIREMENT: Human Gravity presentation metadata must not influence CORE truth/decision/state artifacts; TASK nickname must not affect context_digest
EVIDENCE: current contextDigest serializes nickname for every intent, while CORE_HANDOFF includes context_digest
FORBIDDEN: NEXY.ai mutation; nickname removal from CASUAL; digest guessing; force push; merge without runtime evidence

TEST_COMMIT: 111af31504a2bcc2b028c0a1b39d8e78a7c60f0d
FIX_COMMIT: 0c9dbd6a218a46c86241e7706696b0b1b9c8b4c0
DRAFT_PR: 78
FIX_DETAIL: TASK digest canonicalization forces nickname=null; CASUAL still retains explicit optional nickname presentation metadata.
TEST_INVARIANT: identical TASK text/context must yield identical context_digest with or without nickname.
PR_STATUS_AT_UPDATE: mergeable=true; draft=true; changed_files=2; runtime PASS absent.
VERDICT: IMPLEMENTED_IN_DRAFT / NOT_RUNTIME_VERIFIED
NEXT_ACTION: validate PR 78 when Actions execution resumes; recheck integration file blobs and mergeability immediately before any integration.
