TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
REVIEWER_CHAT: C-9B6A4E27
ROLE: SHADOW_REVIEWER / SECURITY_ORACLE_CHALLENGER
STATUS: PREIMPLEMENTATION_REVIEW
REVIEW_RESULT: CHANGES_REQUIRED
PRIORITY: P1
RISK: HIGH_AUTH_SECURITY
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
BASE_SHA_REVIEWED: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_MUTATION_BY_REVIEWER: NONE

## PRIMARY-SOURCE FACTS
- Final DOC-C POST /api/auth/verify-otac purpose is to verify one-time code and create session.
- Its canonical error matrix contains both 401 AUTH_INVALID and 401 AUTH_EXPIRED.
- Final DOC-C §8.4 states OTAC is one-time use and a reused consumed OTAC => AUTH_INVALID + security audit.
- Primary DOC-C does not explicitly say that mere existence of any expired row makes an arbitrary submitted code AUTH_EXPIRED.

## SOURCE FACTS AT 608426cb30398b1f3461866f7079d2a435c96b96
packages/api/auth.ts:
- rawRows query is ordered createdTick ascending and takes 32.
- live = real row && expiresAt > now.
- expired rows use DUMMY_SALT and DUMMY hash input, so an exact expired credential can never be recognized.
- consumedReplay requires sameDeviceRow, and sameDeviceRow requires live, so replay-after-expiry is not recognized.
- when no eligible live row exists, fallback is 401 AUTH_INVALID.
- packages/api/auth.ts blob is identical on NEXY.ai and NEXY.AI-Test-AI at this baseline.

core-kernel/src/auth/email_gate.rs:
- Rust exposes AuthResult::Expired when email-matching sessions exist but all are expired.
- Rust does not prove the HTTP route's exact wrong-code-vs-expired-code oracle. It is parity evidence only, not authority.

## REVIEW OF EXISTING FINDING
FIND-AUTH-OTAC-EXPIRED-001 is correct that the HTTP route currently has no reachable OTAC-specific AUTH_EXPIRED result.
Its reproduction is overbroad where it says any syntactically valid code against an expired row should return AUTH_EXPIRED.

## REQUIRED ORACLE
FACT:
- Consumed replay remains AUTH_INVALID + security audit, including after expiry, because DOC-C §8.4 provides no expiry exception.

ENGINEERING INFERENCE CONSISTENT WITH THE CANONICAL REQUIREMENT PACKET:
- Exact same-email/same-device, unconsumed expired code/hash match => AUTH_EXPIRED.
- Expired row + wrong code must not become AUTH_EXPIRED solely because the row exists.
- Live wrong code remains AUTH_INVALID.
- Existing OTAC_LOCKED and DEVICE_MISMATCH precedence must not be weakened.

UNKNOWN:
- DOC-C does not spell out a formal precedence table between every combination of expired, consumed, wrong-code, and device-mismatch predicates. The implementation must therefore avoid inventing broader disclosure than needed to make AUTH_EXPIRED reachable.

## SAFE IMPLEMENTATION SHAPE
After branch-policy unblock, keep exactly SESSION_SLOTS iterations and no early return.
For every real row, compute the candidate hash from the real stored salt even when the row is expired; keep dummy hashing only for padding.
Accumulate classification flags during the complete scan, then classify after the scan:
- live unconsumed exact same-device match -> success
- consumed exact same-device match -> AUTH_INVALID + replay security audit
- expired unconsumed exact same-device match -> AUTH_EXPIRED
- otherwise retain existing mismatch / device / invalid behavior
This is a design recommendation, not a source-authority override.

## SECURITY CONSTRAINTS
- Never admit an expired or consumed OTAC.
- Never expose plaintext OTAC.
- Do not add early exits.
- Do not reduce the 32-slot scan.
- Do not skip AUTH_VERIFY_FAILED audit evidence.
- Persistence/audit failure remains fail-closed.

## RESULT
Second independent review: CHANGES_REQUIRED.
Implementation remains blocked by INC-BRANCH-NAMESPACE-001.
