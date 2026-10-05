# F-AUTH-OWNER-RECOVERY-SESSION-BYPASS-001

STATUS: OPEN
SEVERITY: P1
CLASS: AUTHORITY_VIOLATION / SECURITY_DEFECT
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

OBSERVED:
- `POST /api/auth/owner-recovery` is an active mutating route.
- `handleOwnerRecoveryRequest` can revoke currently active sessions with `tx.session.updateMany(...)` and writes incident/event/audit/idempotency records.
- The handler validates CSRF and idempotency but does not require an authenticated secure session before mutation.
- A separate public recovery-CSRF bootstrap endpoint exists specifically so the flow can be initiated without session authority.

EXPECTED:
FINAL DOC-C section 4.1 states that all mutating routes require secure session + CSRF, except OTAC request/verify. `owner-recovery` is not one of those exceptions and is not present in the canonical route matrix.

IMPACT:
An active mutation path operates outside the canonical session authority boundary. Even if its eligibility predicates are intentionally narrow, they do not constitute the secure-session authority required by DOC-C.

REPAIR_DIRECTION:
Fail closed until the route has explicit authoritative exemption or is redesigned to remain non-mutating before authenticated OWNER authority. Do not invent a new exemption in code.

BLOCKED_BY: F-CONTROL-WORKER-REF-NAMESPACE-001
