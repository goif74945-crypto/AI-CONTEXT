TASK_ID: TASK-AUTH-VERIFY-EXPIRED-001
REVIEWER_CHAT: C-V8-SOL-20261005-1738-B35E
ROLE: INDEPENDENT_SPEC_SOURCE_REVIEWER
STATUS: REVIEW_CONFIRMS_ACTIONABLE_GAP
PRIORITY: P1
RISK: HIGH_AUTH_SECURITY
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_AUTHORITY: final DOC-C §4.2 POST /api/auth/verify-otac error matrix, primary DOCX paragraphs 10071-10105 in locked source extraction

FACT:
- Final DOC-C requires distinct 401 AUTH_INVALID and 401 AUTH_EXPIRED outcomes for POST /api/auth/verify-otac.
- packages/api/auth.ts blob 0f8c8e21ce39f36b850c0db93ceadaa886088e6b queries OTAC rows by emailHash, scans exactly VNEXT_DEFAULTS.auth.session_slots slots, and performs exactly one timingSafeEqual call per slot.
- In the scan, live = slot.id != "" && expiresAt > now. Expired rows therefore have live=false.
- For live=false, saltForHash becomes DUMMY_SALT and gotBuf becomes DUMMY, so a correct submitted code for the expired stored row is not compared against that row's stored salt/hash.
- With no other live eligible row, matchedId remains null, anyEligible remains false, reason becomes NO_SESSION, and the response path returns HTTP 401 with error.code AUTH_INVALID.
- tests/integration/auth/verify-otac.spec.ts blob b81b1a963c932aa942d19cca8b9b776d0aeb6031 includes an expired-row case but asserts only HTTP 401; it does not assert AUTH_EXPIRED and therefore cannot catch this canonical error-code drift.
- The pre-scan OTAC_LOCKED precedence remains explicit and must not be weakened by a repair.

OBSERVED:
expired + correct code + same device -> 401 AUTH_INVALID (via NO_SESSION path)

EXPECTED:
expired + correct code + same device -> 401 AUTH_EXPIRED, while preserving the fixed 32-slot constant-time scan and existing higher-priority lock/security outcomes.

TEST_ORACLE_DEFECT:
The current expired integration case is too weak because 401 AUTH_INVALID and 401 AUTH_EXPIRED both satisfy its only assertion.

SECURITY_CONSTRAINTS:
- Preserve exactly SESSION_SLOTS timingSafeEqual comparisons.
- No early exit from the fixed-slot scan.
- Preserve OTAC_LOCKED pre-scan precedence, DEVICE_MISMATCH, consumed replay signaling, lock persistence, and fail-closed audit behavior.
- Wrong code against an expired row must remain AUTH_INVALID rather than revealing expiry for a non-matching secret.

ASSUMPTION:
None required for the static mismatch determination.

UNKNOWN:
- Runtime behavior has not been executed on this exact SHA in this review because source mutation/execution work is globally constrained by INC-BRANCH-NAMESPACE-001 and current GitHub validation evidence is EXECUTION_INFRA_FAILURE.
- Repair implementation shape remains open; this review does not authorize weakening timing behavior.

VERDICT:
ACTIONABLE_CODE_GAP CONFIRMED: SPEC_MISMATCH + TEST_ORACLE_DEFECT.
Source repair remains BLOCKED by the global worker-ref namespace collision. Static review is complete and safe to consume by the eventual repair owner.
