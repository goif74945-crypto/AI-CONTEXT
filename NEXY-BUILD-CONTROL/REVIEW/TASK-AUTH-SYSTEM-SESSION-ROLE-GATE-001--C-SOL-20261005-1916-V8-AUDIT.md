# Second Independent Review — TASK-AUTH-SYSTEM-SESSION-ROLE-GATE-001

REVIEW_ID: RVW-AUTH-SYSTEM-SESSION-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-AUTH-SYSTEM-SESSION-ROLE-GATE-001
FINDING_ID: FINDING-DOC-C-ROLE-SYSTEM-SESSION-AUTHORITY-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: INDEPENDENT_AUTHORITY_REVIEWER / RED_TEAM
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## PRIMARY AUTHORITY
Final DOC-C POST /api/auth/verify-otac success role union is OWNER | OPERATOR | AUDITOR.
Final DOC-C GET /api/session/me requires session, declares RBAC OWNER | OPERATOR | AUDITOR, and returns the same role union.
Final DOC-C separately authorizes SYSTEM for POST /api/vault/commit, so SYSTEM cannot be removed globally merely to repair these interactive routes.

## EXACT-HEAD SOURCE PROOF
packages/api/auth.ts blob 0f8c8e21ce39f36b850c0db93ceadaa886088e6b:
- loads userRecord as { id, role: Role };
- selects const role: Role = userRecord?.role ?? Role.AUDITOR;
- passes that role unchanged into tx.session.create(... role ...);
- records AUTH_VERIFIED with that role;
- returns role in the HTTP 200 verify-otac success envelope;
- handleSessionMe reads persisted session.role and returns it in HTTP 200 after session/revocation/expiry/device/user-binding checks, with no route-local OWNER/OPERATOR/AUDITOR gate.

prisma/schema.prisma blob 0c557a1bb9b02859bb479655575c3566e201eb6f permits SYSTEM in Role, User.role, and Session.role. Therefore a durable SYSTEM user/session is representable and the route-local gap is executable, not merely a type-theory concern.

## TEST PROOF
tests/integration/auth/verify-otac.spec.ts blob b81b1a963c932aa942d19cca8b9b776d0aeb6031 contains no SYSTEM case.
tests/coverage/auth-decision-paths.test.ts blob 3cefe463642b43735c5e61cd018dcd9fae3d6967 tests SYSTEM rejection only for logout. Its verify-otac and session-me sections have no negative SYSTEM boundary case.

## VERDICT
VERIFY_OTAC_SYSTEM_SUCCESS_PATH: CONFIRMED
SESSION_ME_SYSTEM_SUCCESS_PATH: CONFIRMED
AUTHORITY_VIOLATION: CONFIRMED_P0
MISSING_NEGATIVE_TESTS: CONFIRMED
GLOBAL_ROLE_MODEL_DEFECT: NOT_PROVEN
IMPLEMENTATION_DENIAL_STATUS_ERROR: UNRESOLVED_BY_FINAL_DOC_C
REVIEW_RESULT: P0_CONFIRMED_IMPLEMENTATION_AUTHORITY_PARTIAL

## SCOPE / AUTHORITY GUARD
The route-local role restriction is directly proven and does not depend on whether the displayed success object is a closed/no-extra-members type. Do not conflate this P0 role-boundary defect with the separate verify success-wire exactness dispute.

Do not silently choose FORBIDDEN, AUTH_INVALID, AUTH_EXPIRED, SESSION_REVOKED, or another code for SYSTEM rejection unless active authority establishes that mapping. The verify route's printed error matrix does not list FORBIDDEN, and session/me does not print a complete route-local error matrix. Freeze only denial-surface design while preserving the confirmed obligation that SYSTEM cannot reach a successful interactive response.

## BLOCKERS
- INC-BRANCH-NAMESPACE-001: mandated worker prefix remains Git-invalid while refs/heads/NEXY.AI-Test-AI exists.
- ACTIVE_AUTH_HOTSPOT: packages/api/auth.ts has overlapping active auth scopes; one semantic writer only.

SOURCE_MUTATION remains forbidden until both isolation and hotspot ownership are reconciled.
