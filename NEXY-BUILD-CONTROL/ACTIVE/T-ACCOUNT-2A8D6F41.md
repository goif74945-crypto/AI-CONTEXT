TASK_ID: T-ACCOUNT-2A8D6F41
CREATOR_CHAT: C-SOL-20261006-ACCOUNT-2A8D6F41
OWNER_CHAT: C-SOL-20261006-ACCOUNT-2A8D6F41
STATUS: IMPLEMENTING
PRIORITY: P2
RISK: LOW
BASE_SHA: 88afb720868754b9c9058868192da1237e545a59
SEMANTIC_SCOPE: Materialize the required DOC-C UI screen "Session / account status" as a read-only backend-truth surface.
TARGET_PATHS:
- apps/web/app/account/page.tsx
- apps/web/components/NavBar.tsx
- tests/contract/session-account-screen.test.ts
AUTHORITY:
- Authoritative DOCX DOC-C §16.2 Screen Inventory includes "Session / account status".
- GET /api/session/me canonical response exposes user_id, role, session_id, expires_at.
REQUIRED_BEHAVIOR:
- /account fetches GET /api/session/me with same-origin credentials and no-store cache.
- Render only canonical user_id, role, session_id, expires_at from backend truth.
- Loading and backend error states must not fabricate authenticated status.
- Primary navigation exposes ACCOUNT without adding new privilege.
FORBIDDEN:
- No auth/session mutation.
- No logout/revoke/refresh controls.
- No API contract changes.
- No NEXY.ai mutation.
- No unrelated NavBar/sidebar behavior changes.
TEST_PLAN:
- Focused source-contract regression for route, canonical fetch/fields and navigation.
- Exact diff and overlap review.
- Exact-head runtime evidence only if execution layer produces steps; do not fabricate.
