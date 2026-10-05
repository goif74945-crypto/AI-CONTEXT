# Shadow Review — GET /api/session/me RBAC

CHAT_ID: C-3B5E71A2
TASK_ID: TASK-DOC-C4-SESSION-ME-RBAC-001
FINDING_ID: FINDING-DOC-C4-SESSION-ME-RBAC-001
REQ_ID: REQ-DOC-C-4-2-SESSION-ME-RBAC-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
AUTH_BLOB: 0f8c8e21ce39f36b850c0db93ceadaa886088e6b
PRISMA_BLOB: 0c557a1bb9b02859bb479655575c3566e201eb6f
ROLE: SHADOW_REVIEWER
VERDICT: FINDING_CONFIRMED_P1
ERROR_ORACLE: FROZEN_BY_SPEC_CONFLICT

## Authoritative facts

Final DOC-C GET /api/session/me:
- session required
- RBAC OWNER / OPERATOR / AUDITOR
- success role union OWNER | OPERATOR | AUDITOR
- success data includes user_id, role, session_id, expires_at

The same final DOC-C route block has no route-local Errors section before POST /api/auth/logout begins. Therefore the exact denial status/code for an otherwise-valid SYSTEM session is not specified by this route block.

## Exact-head reachability

- Prisma Role includes SYSTEM.
- Session.role uses the full Role enum.
- handleVerifyOtac derives role from the durable User record and writes that Role directly into Session.role.
- handleSessionMe validates cookie, persistence, revoked/expired state, device binding and user binding, then serializes session.role without an allow-list.
- Therefore a persisted SYSTEM user can produce a valid authenticated SYSTEM session and receive HTTP 200 with role=SYSTEM from GET /api/session/me.
- Existing focused tests cover AUDITOR success but do not reject SYSTEM.

## Repair boundary

The success-authority defect can be fixed without changing persistence:
- after existing session/device/user-binding checks and before the 200 response, enforce role membership in OWNER/OPERATOR/AUDITOR;
- never serialize SYSTEM in the canonical 200 data;
- add OWNER, OPERATOR, AUDITOR positive tests and SYSTEM negative test;
- preserve all existing missing-cookie, revoked, expired, device mismatch, missing-user-binding and dependency-failure behavior.

The exact HTTP status/ErrorCode for the SYSTEM denial MUST NOT be invented while F-C-SOL-V8-1737-SESSION-ME-ERROR-MATRIX-CONFLICT remains unresolved. A code patch that chooses an endpoint-specific denial pair and labels it final DOC-C would exceed authority.

SOURCE_MUTATION: NONE
UPSTREAM_MUTATION: NONE
MUTATION_BLOCKER: INC-BRANCH-NAMESPACE-001
ADDITIONAL_BLOCKER: F-C-SOL-V8-1737-SESSION-ME-ERROR-MATRIX-CONFLICT for exact denial oracle only
