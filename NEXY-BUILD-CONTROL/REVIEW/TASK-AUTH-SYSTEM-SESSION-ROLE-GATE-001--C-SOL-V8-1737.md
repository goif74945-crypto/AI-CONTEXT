REVIEW_ID: R-AUTH-SYSTEM-SESSION-C-SOL-V8-1737-001
TASK_ID: TASK-AUTH-SYSTEM-SESSION-ROLE-GATE-001
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
REVIEWER: C-SOL-V8-1737
ROLE: INDEPENDENT_AUTHORITY_REVIEWER / RED_TEAM
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
RESULT: FINDING_CONFIRMED_REPAIR_CONTRACT_INCOMPLETE
SOURCE_MUTATION: NONE

DIRECT AUTHORITY:
- final DOC-C POST /api/auth/verify-otac success data restricts role to OWNER | OPERATOR | AUDITOR.
- final DOC-C GET /api/session/me RBAC and response data restrict role to OWNER | OPERATOR | AUDITOR.
- final DOC-C does not authorize SYSTEM as an interactive session role on either route.
- final DOC-C separately authorizes SYSTEM on specific non-interactive paths such as vault commit; that does not widen auth-session routes.

SOURCE FACT:
- Prisma Role includes SYSTEM.
- handleVerifyOtac obtains role directly from durable User.role, then persists it into Session.role and returns it in the success envelope.
- no route-local gate prevents a durable SYSTEM user from reaching that success path.
- handleSessionMe validates session existence/revocation/expiry/device/user binding but then returns session.role directly with no OWNER/OPERATOR/AUDITOR gate.
- current auth coverage has no negative SYSTEM case for verify-otac or session-me.

VERDICT:
FINDING-DOC-C-ROLE-SYSTEM-SESSION-AUTHORITY-001 is a valid P0 authority gap. The global role model does not need to be narrowed; the defect is at the interactive route boundary.

REPAIR CONSTRAINTS:
1. POST /api/auth/verify-otac must never create or return a SYSTEM interactive session.
2. GET /api/session/me must never return a successful SYSTEM session response.
3. Do not remove SYSTEM from the global Prisma/contract role model solely for this repair because final DOC-C separately uses SYSTEM authority on other paths.
4. Do not silently coerce SYSTEM to AUDITOR/OPERATOR/OWNER. That would fabricate authority.
5. Preserve OWNER/OPERATOR/AUDITOR behavior, session/device checks, OTAC consumption semantics and audit requirements.
6. Add negative tests using a durable SYSTEM user and a persisted SYSTEM session.

UNRESOLVED ERROR-SURFACE DETAIL:
- verify-otac's explicit canonical errors are AUTH_INVALID, AUTH_EXPIRED, DEVICE_MISMATCH, OTAC_LOCKED and SESSION_REVOKED; FORBIDDEN is not listed for this public route.
- session/me states RBAC OWNER/OPERATOR/AUDITOR but final DOC-C does not print a route-local error list immediately after its response.
Therefore the denial status/error code for SYSTEM must be independently fixed before implementation. The repair may not invent a new success role or widen the route error contract merely for convenience.

IMPLEMENTATION_APPROVAL: NO
UNBLOCK_FOR_DESIGN_APPROVAL:
- select and justify the canonical denial behavior for SYSTEM at verify-otac and session/me;
- then re-review before source mutation.
