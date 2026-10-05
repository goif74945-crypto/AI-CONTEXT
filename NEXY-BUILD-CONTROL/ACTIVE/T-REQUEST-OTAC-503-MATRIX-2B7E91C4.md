TASK_ID: T-REQUEST-OTAC-503-MATRIX-2B7E91C4
OWNER_CHAT: C-SOL-20261006-0132
STATUS: RELEASED_TO_RUNTIME_VALIDATION
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-4-2-REQUEST-OTAC
FINDING_ID: F-CV8-OTAC-503-MATRIX-01
TARGET_PATHS:
- packages/api/middleware/rate-limit.ts
- tests/coverage/rate-limit-branches.test.ts
RED_TEST_COMMIT: a0efe4165f9d8d4cbc8c0d26c2a0e33ab4c13433
SOURCE_FIX_COMMIT: 0828481b36b6f252146b07ace40dd4cd0d759ad4
STATIC_EVIDENCE:
- exactly two dependency-unhealthy failure sites now map request_otac profile to DEPENDENCY_FAILURE
- non-request_otac profiles retain DEPENDENCY_UNHEALTHY
- fail-closed behavior and rate-limit quotas/signals unchanged
- tests cover runtime-config failure, Redis fail-closed, and profile isolation
GITHUB_ACTIONS_EVIDENCE:
- red-test exact/six runs 37361751673 / 37361751566 failed before first step, stepCount=0
- source-fix exact/six runs 37361772882 / 37361773041 observed queued with stepCount=0 at release time
RUNTIME_VERDICT: NOT_VERIFIED
MUTATION_OWNER_ACTIVE: FALSE
UNRESOLVED_SEPARATE_SCOPE: verify-OTAC admission/error/audit authority conflict remains frozen; this task does not claim to solve it.
