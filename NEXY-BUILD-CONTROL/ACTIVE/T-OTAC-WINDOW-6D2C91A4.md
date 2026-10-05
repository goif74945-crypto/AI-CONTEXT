TASK_ID: T-OTAC-WINDOW-6D2C91A4
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
SEMANTIC_SCOPE: Guarantee newest valid active OTAC remains in the fixed-width verification candidate window despite retained historical rows.
TARGET_PATHS:
- packages/api/auth.ts
- tests/coverage/auth-decision-paths.test.ts
MUTATION_BOUNDARY: Change only verification candidate ordering from oldest-first to newest-first and add a focused regression/assertion. Preserve fixed SLOTS scan width, lockout, replay, device mismatch, TTL, session creation, and AUTH_EXPIRED mapping unchanged.
FORBIDDEN:
- No NEXY.ai mutation.
- No change to SESSION_SLOTS=32 hardening.
- No change to expired-code error classification in this task.
BASE_EVIDENCE: current branch blob packages/api/auth.ts uses orderBy createdTick asc + take SLOTS, reproducing retained-history starvation counterexample.
