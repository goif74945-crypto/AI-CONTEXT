TASK_ID: TASK-AUTH-LOGOUT-IDEMPOTENCY-PRINCIPAL-BINDING-001
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-4-2-AUTH-LOGOUT-IDEMPOTENCY
FINDING_ID: FINDING-AUTH-LOGOUT-IDEMPOTENCY-PRINCIPAL-BINDING-001
SEMANTIC_SCOPE: Bind logout idempotency replay to the exact authenticated session/principal and exact revoke_all semantics using existing accepted AuditLog evidence.
TARGET_PATHS:
- packages/api/auth.ts
- tests/integration/auth/logout.spec.ts
REQUIRED:
- resolve and device-bind the current session before trusting prior idempotency evidence
- prior evidence must match exact action, current session resourceId, current principal actor, and ACCEPTED outcome
- same exact retry remains 200 without duplicate revoke mutation
- cross-session/principal or revoke_all variant collision must execute current revocation rather than false-replay
- preserve CSRF, RBAC, device binding, revocation, audit names, fail-closed persistence
FORBIDDEN:
- no NEXY.ai mutation
- no schema/store invention
- no weakening of revoked-session misuse detection for non-idempotent requests
BASE_EVIDENCE: current auth.ts still performs broad requestId + action IN [AUTH_LOGOUT, AUTH_LOGOUT_ALL] lookup before session resolution.
