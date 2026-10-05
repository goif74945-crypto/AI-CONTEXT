# Independent Review — TASK-DOC-C4-CANONICAL-ROUTE-ORACLE-001

REVIEW_ID: RVW-DOC-C4-CANONICAL-ROUTES-C-SOL-20261005-1916-V8-AUDIT
TASK_ID: TASK-DOC-C4-CANONICAL-ROUTE-ORACLE-001
FINDING_ID: FINDING-DOC-C4-CANONICAL-ROUTE-ORACLE-001
REVIEWER_CHAT: C-SOL-20261005-1916-V8-AUDIT
ROLE: SHADOW_REVIEW / SPEC_AUDIT / CONTRACT_AUDIT
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_MUTATION: NONE

## FINAL DOC-C ROUTE DENOMINATOR
Raw 10038-10352 contains exactly these twelve §4.2 routes:
1. POST /api/auth/request-otac
2. POST /api/auth/verify-otac
3. GET /api/session/me
4. POST /api/auth/logout
5. POST /api/directives
6. GET /api/directives/:id
7. GET /api/runs/:id
8. POST /api/freeze/recover
9. POST /api/vault/commit
10. GET /api/artifacts/:id/revisions
11. GET /api/incidents/:id
12. GET /api/audit-logs

## EXACT-HEAD ORACLE REVIEW
scripts/check-doc-c.ts blob 5d60b3b8bcce8d11988fd971679eb9685177cc43 defines fifteen canonical route checks by additionally promoting:
- GET /api/directives
- GET /api/runs
- GET /api/artifacts
No active final-DOC-C §4.2 clause for those three collection routes was found.

The checker validates the route adapter primarily by exported HTTP method existence. That proves adapter presence, not §4.2 auth/RBAC/idempotency/audit/error semantics.

tests/contract/canonical-api.test.ts does exercise several handler semantics, but it also directly tests implementation-only collection handlers and does not provide a single exact twelve-route authority denominator.

## VERDICT
FINAL_DOC_C_ROUTE_COUNT: 12
CURRENT_STATIC_ORACLE_ROUTE_COUNT: 15
ORACLE_AUTHORITY_DRIFT: CONFIRMED
SEMANTIC_ROUTE_ORACLE: INCOMPLETE
IMPLEMENTATION_ONLY_ENDPOINT_DELETION_REQUIRED: NO
TASK_DESIGN: APPROVED
EXECUTED_TEST_EVIDENCE: NOT_AVAILABLE
REVIEW_RESULT: INDEPENDENTLY_CONFIRMED_STATIC_GAP

## SCOPE GUARD
scripts/check-doc-c.ts also contains state/event assertions outside this task. Do not opportunistically rewrite those assertions under the canonical-route task; state/event authority has separate active scopes and owners. Minimal repair should change only the canonical route denominator and route-semantic oracle evidence required by this task.

GLOBAL_BLOCKER: INC-BRANCH-NAMESPACE-001 prevents isolated source/test mutation until the worker namespace law becomes Git-valid.
