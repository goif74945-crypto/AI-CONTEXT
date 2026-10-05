TASK_ID: T-OTAC-WINDOW-6D2C91A4
OWNER_CHAT: C-SOL-20261006-0132
STATUS: RELEASED_TO_RUNTIME_VALIDATION
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
SEMANTIC_SCOPE: Guarantee newest valid active OTAC remains in the fixed-width verification candidate window despite retained historical rows.
TARGET_PATHS:
- packages/api/auth.ts
- tests/coverage/auth-decision-paths.test.ts
SOURCE_COMMIT: e57786eb98fa1aea78f3faf857b6ac55f0ad93de
TEST_COMMIT: cf2da83c1a56fedbdb8812e4d2664d39ce7cc8cc
STATIC_EVIDENCE:
- verification query now orders OtacPending by createdTick desc and still takes exactly SLOTS
- focused coverage regression requires orderBy createdTick desc and take 32
- descendant HEAD abe403615f8037dd1870839fd5e45ea317744118 retained the source behavior and regression
GITHUB_ACTIONS_EVIDENCE:
- exact-head run 37359044669: failure before first step, stepCount=0
- six-system run 37359044697: failure before first step, stepCount=0
RUNTIME_VERDICT: NOT_VERIFIED
MUTATION_OWNER_ACTIVE: FALSE
NEXT_ACTION: execute focused auth coverage/integration tests on an execution plane that reaches test steps; do not infer PASS from static evidence.
