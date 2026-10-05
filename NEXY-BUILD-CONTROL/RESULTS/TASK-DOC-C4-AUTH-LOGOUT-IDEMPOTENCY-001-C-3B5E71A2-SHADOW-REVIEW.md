# Shadow Review — Logout Idempotency Binding

CHAT_ID: C-3B5E71A2
TASK_ID: TASK-DOC-C4-AUTH-LOGOUT-IDEMPOTENCY-001
FINDING_ID: FINDING-DOC-C4-AUTH-LOGOUT-IDEMPOTENCY-001
REQ_ID: REQ-DOC-C-4-CANONICAL-ROUTE-SURFACE
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_BLOB_AUTH: 0f8c8e21ce39f36b850c0db93ceadaa886088e6b
SOURCE_BLOB_SCHEMA: 0c557a1bb9b02859bb479655575c3566e201eb6f
TEST_BLOB: 3cefe463642b43735c5e61cd018dcd9fae3d6967
ROLE: SHADOW_REVIEWER
VERDICT: FINDING_CONFIRMED_P1

## Reproduction by exact-SHA control flow

1. Caller supplies a valid secure session/device binding and logout body with idempotency key K.
2. handleLogout queries AuditLog by requestId=K and action IN [AUTH_LOGOUT, AUTH_LOGOUT_ALL] without principal/session/action-exact binding.
3. Session and device binding for the current caller are then validated.
4. If any unrelated accepted logout audit row with K exists, the prior branch returns HTTP 200 with revoked=true before checking current session revoked/expired/role and before any revocation mutation.
5. AuditLog has resourceId and actor fields that already carry session.id and emailHash for successful logout rows, so a safe binding can be expressed without a schema migration.

## Minimal repair design

- Keep CSRF validation first.
- Parse body and derive exact action from revoke_all.
- Load the current session and validate the device binding.
- Query prior accepted logout evidence using all available request identity:
  - requestId = idempotency_key
  - action = exact current action, not action IN both variants
  - resourceKind = Session
  - resourceId = current session.id
  - actor = current session.emailHash (defense-in-depth)
  - outcome = ACCEPTED
- Keep the exact-prior branch before revoked/expired checks so a retry of the original accepted request still returns the prior success even though the original session was revoked by that request.
- If no exact prior exists, preserve current revoked/expired/RBAC checks and transactional mutation path.

## Required regression cases

- same key + same session + same revoke_all after successful logout => 200 prior success, no second mutation
- same key + different session same principal => must not false-success
- same key + different principal => must not false-success
- same key + same session but opposite revoke_all => must not cross-action replay
- prior lookup persistence failure => fail closed
- device mismatch => denied before prior-success replay
- exact prior with already-revoked original session => still returns prior accepted result

## Boundary

SOURCE_MUTATION: NONE
UPSTREAM_MUTATION: NONE
MUTATION_BLOCKER: INC-BRANCH-NAMESPACE-001
