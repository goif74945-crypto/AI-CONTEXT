TASK_ID: T-AUTH-EXPIRED-91E4C2B7
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
SEMANTIC_SCOPE: Make POST /api/auth/verify-otac return canonical 401 AUTH_EXPIRED only for an exact same-device unconsumed expired OTAC match, preserving constant-width security behavior.
TARGET_PATHS:
- packages/api/auth.ts
- tests/coverage/auth-decision-paths.test.ts
- tests/integration/auth/verify-otac.spec.ts
AUTHORITY:
- Final DOC-C verify-otac error surface contains AUTH_INVALID and AUTH_EXPIRED.
- Independent reviews C-71A0F5E7, C-9B6A4E27, C-V8-SOL-20261005-1738-B35E converge on exact-expired-match classification.
REQUIRED:
- exactly SLOTS timingSafeEqual calls; no early exit
- exact same-device + unconsumed + expired + matching code => 401 AUTH_EXPIRED
- expired wrong code => AUTH_INVALID
- consumed exact replay => AUTH_INVALID plus existing security signal, including after expiry
- OTAC_LOCKED pre-scan precedence unchanged
- DEVICE_MISMATCH existing precedence unchanged
- audit/persistence failures remain fail-closed
FORBIDDEN:
- No NEXY.ai mutation
- no plaintext OTAC exposure
- no acceptance of expired/consumed code
- no arbitrary expired-row existence => AUTH_EXPIRED
