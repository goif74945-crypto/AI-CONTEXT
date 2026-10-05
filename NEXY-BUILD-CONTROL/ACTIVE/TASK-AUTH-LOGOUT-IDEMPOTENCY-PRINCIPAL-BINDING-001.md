TASK_ID: TASK-AUTH-LOGOUT-IDEMPOTENCY-PRINCIPAL-BINDING-001
OWNER_CHAT: C-SOL-20261006-0132
STATUS: RELEASED_TO_RUNTIME_VALIDATION
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-4-2-AUTH-LOGOUT-IDEMPOTENCY
FINDING_ID: FINDING-AUTH-LOGOUT-IDEMPOTENCY-PRINCIPAL-BINDING-001
TARGET_PATHS:
- packages/api/auth.ts
- tests/integration/auth/logout.spec.ts
RED_ORACLE_COMMIT: 77519350b839fe9371d2f80655495ab13d3b90a7
SOURCE_FIX_COMMIT: c2a833cde90a51d7fd709937d66a4abea132739e
COUNTEREXAMPLE_TEST_COMMIT: 132b695abceac01c4448d6c806db1294e0a1cac9
STATIC_EVIDENCE:
- broad action IN lookup removed
- prior evidence lookup occurs only after current session resolution and device binding
- lookup binds requestId, exact action, session.emailHash actor, session.id resourceId, ACCEPTED outcome
- prior replay remains before revoked-session misuse branch so legitimate same-operation retries can return 200 without duplicate mutation
- tests cover exact lookup shape, same accepted replay, cross-session/principal collision, and revoke_all/single-session action collision
GITHUB_ACTIONS_EVIDENCE:
- red-oracle runs 37360964277 / 37360964315 failed before first step, stepCount=0
- source-fix runs 37361008361 / 37361008356 failed before first step, stepCount=0
- latest exact-head run 37361079406 observed queued with stepCount=0 at release time
RUNTIME_VERDICT: NOT_VERIFIED
MUTATION_OWNER_ACTIVE: FALSE
NEXT_ACTION: execute tests/integration/auth/logout.spec.ts plus auth security suite when an execution plane can run steps; do not infer PASS from static evidence.
