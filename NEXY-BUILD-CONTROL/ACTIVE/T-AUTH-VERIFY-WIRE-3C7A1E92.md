TASK_ID: T-AUTH-VERIFY-WIRE-3C7A1E92
OWNER_CHAT: C-SOL-20261006-0132
STATUS: CONVERGED_BY_CONCURRENT_WORK
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-4-2-VERIFY-OTAC
FINDING_ID: FINDING-DOC-C4-VERIFY-OTAC-RESPONSE-SHAPE-001
SEMANTIC_SCOPE: Align successful POST /api/auth/verify-otac response data exactly to final DOC-C fields session_id, expires_at, role.
TARGET_PATHS:
- packages/api/auth.ts
- tests/coverage/auth-decision-paths.test.ts
- tests/integration/auth/verify-otac.spec.ts
REQUIRED:
- continue issuing CSRF cookie on every successful verify
- data contains only session_id, expires_at, role
- no email_hash or csrf_token in verify response body
- session/auth/role/device-binding behavior unchanged
EVIDENCE:
- final DOC-C paragraphs 10092-10098 declare only session_id, expires_at, role
- repository-wide search found no consumer of verify response data.csrf_token/email_hash
- packages/auth/csrf.ts sets __Host-nexy-csrf with httpOnly=false, so SPA can read the double-submit cookie
FORBIDDEN:
- no NEXY.ai mutation
- no change to session-refresh or owner-recovery route shapes in this task

STATUS_RESOLUTION: CONVERGED_BY_CONCURRENT_WORK
SOURCE_MUTATION_BY_THIS_CHAT: NONE
LATEST_STATIC_EVIDENCE:
- packages/api/auth.ts response data now contains only session_id, expires_at, role
- tests/coverage/auth-decision-paths.test.ts now asserts exact success data and CSRF issuance out-of-band
MUTATION_OWNER_ACTIVE: FALSE
NEXT_ACTION: runtime verification only; do not duplicate source mutation.
