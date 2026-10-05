TASK_ID: T-REQUEST-OTAC-503-MATRIX-2B7E91C4
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-4-2-REQUEST-OTAC
FINDING_ID: F-CV8-OTAC-503-MATRIX-01
SEMANTIC_SCOPE: Align only request_otac rate-limit dependency failures with the route-declared 503 DEPENDENCY_FAILURE pair.
TARGET_PATHS:
- packages/api/middleware/rate-limit.ts
- tests/coverage/rate-limit-branches.test.ts
REQUIRED:
- runtime config failure under runtimeProfile=request_otac => 503 DEPENDENCY_FAILURE
- Redis fail-closed under runtimeProfile=request_otac => 503 DEPENDENCY_FAILURE
- admission remains fail-closed
- other profiles retain their existing dependency code pending separate authority resolution
FORBIDDEN:
- no weakening rate limits
- no verify-otac error-matrix invention
- no change to request-OTAC 429 behavior or audit semantics in this task
- no NEXY.ai mutation
CONFLICT_CHECK: prior T-C84E61B2 is ACTIVE=false / mutation released.
