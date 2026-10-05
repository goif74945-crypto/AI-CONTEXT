TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
REVIEWER_CHAT: C-71A0F5E7
ROLE: SHADOW_REVIEWER / SECURITY_ORACLE_CHALLENGER
STATUS: PREIMPLEMENTATION_REVIEW
REVIEW_RESULT: CHANGES_REQUIRED
PRIORITY: P1
RISK: HIGH_AUTH_CLASSIFICATION
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
BASE_SHA_REVIEWED: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_MUTATION_BY_REVIEWER: NONE

FACT:
- Final DOC-C POST /api/auth/verify-otac lists both 401 AUTH_INVALID and 401 AUTH_EXPIRED (authoritative DOCX paragraphs 10071-10105).
- Final DOC-C §8.4 states: reusing a consumed OTAC => AUTH_INVALID + security audit (paragraphs 10853-10860).
- At 608426cb, handleVerifyOtac marks a row live only when expiresAt > now; expired rows are therefore excluded from anyEligible and anySameDeviceEligible.
- At 608426cb, expired rows are also hashed against DUMMY_SALT/DUMMY rather than their stored salt/hash, so the handler cannot distinguish an exact expired-code submission from an arbitrary wrong code when only expired rows exist.
- The current no-match fallback returns AUTH_INVALID when anyEligible=false.
- consumedReplay is currently detected only on live rows; an exact replay of a consumed row after expiry cannot reach the explicit OTAC_REPLAY security-audit path.

UNSUPPORTED_ORACLE IN CURRENT FINDING:
FIND-AUTH-OTAC-EXPIRED-001 reproduction says an expired row plus "any syntactically valid OTAC" should return AUTH_EXPIRED. Primary DOC-C does not state that mere existence of an expired row makes every submitted code AUTH_EXPIRED. That expectation would collapse invalid-code and expired-code classification and may reveal issuance/expiry state for arbitrary guesses.

REQUIRED_ORACLE:
1. Use an exact code/hash match when proving AUTH_EXPIRED. The test fixture must construct the stored hash from the submitted code, email binding, device binding and salt, then set expiresAt <= now and consumed=false.
2. A live same-device wrong code remains AUTH_INVALID and continues the canonical attempt/lock path.
3. A consumed-code replay remains AUTH_INVALID + security audit per §8.4; do not let AUTH_EXPIRED swallow replay classification.
4. DEVICE_MISMATCH and OTAC_LOCKED remain higher-specificity outcomes when their existing authoritative predicates are satisfied.
5. Preserve fixed-width constant-time scanning. Expiry classification must not add an early exit or variable slot count.
6. Do not return AUTH_EXPIRED solely because any expired row exists. If implementation cannot prove the submitted credential corresponds to that expired OTAC, treat the classification as UNKNOWN rather than inventing certainty.

ENGINEERING_INFERENCE:
A safe implementation can still scan exactly SESSION_SLOTS and compute timing-safe comparisons for every real row, including expired rows, while never admitting an expired match. After the full scan it can classify an exact unconsumed same-device expired match as AUTH_EXPIRED. Padding remains dummy-backed. This is a design option, not primary-source authority.

SEPARATE SECURITY GAP:
Current consumedReplay detection is gated by live expiry. DOC-C §8.4 contains no expiry exception for replay auditing. Exact consumed replay after expiry therefore appears to miss the required security-audit path at 608426cb. Track this as a distinct finding rather than silently widening the expired-auth repair.

ACCEPTANCE BEFORE PASS:
- Red-first exact-expired-match test fails on 608426cb with AUTH_INVALID and expects AUTH_EXPIRED.
- Wrong-code-only-expired-row test does not assert AUTH_EXPIRED without additional authority evidence.
- Live wrong-code / device mismatch / active lock / consumed replay cases remain explicit.
- Constant-width scan remains exactly VNEXT_DEFAULTS.auth.session_slots with no early return.
- Exact worker-candidate SHA executes affected auth tests once INC-BRANCH-NAMESPACE-001 is resolved.
