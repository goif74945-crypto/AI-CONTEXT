# F-AUTH-SYSTEM-OTAC-SESSION-001

STATUS: OPEN
SEVERITY: P1
CLASS: AUTHORITY_VIOLATION / UNHANDLED_REQUIRED_STATE / CONTRACT_DRIFT
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

OBSERVED:
- Prisma `Role` permits OWNER, OPERATOR, AUDITOR, and SYSTEM.
- `handleVerifyOtac` loads `User.role` and uses it directly as the new session role without rejecting `Role.SYSTEM`.
- The created session, AUTH_VERIFIED event/audit row, and HTTP response all propagate that role.
- FINAL DOC-C `POST /api/auth/verify-otac` response role union is OWNER | OPERATOR | AUDITOR; `GET /api/session/me` declares the same human-session role union.
- OWNER role-management input is limited to OWNER/OPERATOR/AUDITOR, but that does not protect auth from a SYSTEM user row created by another internal/migration path permitted by the DB schema.

EXPECTED:
Human OTAC authentication must fail closed if durable role is outside the canonical human-session role set. SYSTEM authority must not silently become a browser/user session unless an explicit authoritative mechanism defines that behavior.

IMPACT:
A datastore-valid SYSTEM principal can cross into the human session/auth surface and violate the declared API contract and authority boundary.

BLOCKED_BY: F-CONTROL-WORKER-REF-NAMESPACE-001
