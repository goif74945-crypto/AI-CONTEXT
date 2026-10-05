FINDING_ID: F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
FROM: C-71A0F5E7
TO: MISSION-AUTH-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P1
STATUS: OPEN
TYPE: SECURITY_AUDIT_GAP

OBSERVED:
packages/api/auth.ts fixed-slot verify logic defines live = real && expiresAt > now. consumedReplay is computed from sameDeviceRow && consumed && isMatch, where sameDeviceRow itself requires live. Expired rows use DUMMY_SALT/DUMMY for comparison. Therefore a previously consumed OTAC submitted again after its expiry cannot be recognized as OTAC_REPLAY and does not enter persistSuspiciousAuthOrFail(... OTAC_REPLAY ...).

EXPECTED:
Final DOC-C §8.4 OTAC Replay Prevention states OTAC is one-time use and "Reusing consumed OTAC => AUTH_INVALID + security audit". No expiry exception is stated.

SPEC_EVIDENCE:
- authoritative spec SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- final DOC-C §8.4 paragraphs 10853-10860
- verify route errors paragraphs 10071-10105

REPRODUCTION:
1. At 608426cb create one same-email/same-device OTAC row with consumed=true, expiresAt <= now, valid stored salt/hash for the submitted code.
2. Submit that exact code to handleVerifyOtac.
3. Current scan substitutes DUMMY_SALT/DUMMY because the row is expired, so consumedReplay remains false.
4. Handler falls through the generic no-active-session AUTH_INVALID path without OTAC_REPLAY suspicious-auth evidence.
5. Expected response code remains AUTH_INVALID, but §8.4 additionally requires security audit for reuse of a consumed OTAC.

BOUNDARY:
Do not fix this by accepting expired/consumed credentials or by returning AUTH_EXPIRED for consumed replay. The missing behavior is replay recognition/audit while preserving rejection.

BLOCKER:
INC-BRANCH-NAMESPACE-001 blocks V7-compliant source mutation; review/test design can continue.
