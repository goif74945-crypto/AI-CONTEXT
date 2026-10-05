TASK_ID: TASK-DOC-C-ROLE-ENUM-001
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
GOAL: Reverify active final-DOC-C role enforcement and determine whether PUBLIC_USER acceptance in the shared RoleSchema creates a real route-level authority gap.
SCOPE: packages/contracts/envelope.ts; active role consumers; tests/contract/envelope.test.ts; tests/integration/directives/read-auth.spec.ts; final-DOC-C role-bearing routes only
ACCEPTANCE:
- No source mutation is justified solely by the non-DOC-C storage enum at paragraph 10726.
- Inventory active consumers of RoleSchema on NEXY.AI-Test-AI exact HEAD.
- For every final-DOC-C protected route, prove that accepted roles match that route's explicit RBAC/response contract.
- If PUBLIC_USER is accepted by any final-DOC-C path that forbids it, create a narrowly scoped source repair task with direct spec evidence.
- If no such active path exists, close the prior exact-global-enum repair premise as unsupported rather than deleting PUBLIC_USER speculatively.
EVIDENCE_TARGET: exact consumer paths; exact branch/SHA; route-local spec clauses; targeted authorization tests; no inference from DOC-D/storage-law enum
PRIORITY: P1_REVERIFY
RISK: HIGH_AUTHORITY_ORACLE
STATUS: CLOSED_GLOBAL_ENUM_REPAIR_PREMISE_UNSUPPORTED
OWNER: C-SOL-20261005-1921-V8-ROLE-REVERIFY
MUTATION_LEASE: NONE
BASE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_MUTATION_BLOCKER: INC-BRANCH-NAMESPACE-001
BLOCKER_NOTE: V8 retains worker prefix NEXY.AI-Test-AI/work/<TASK_ID>, which is structurally incompatible with the existing refs/heads/NEXY.AI-Test-AI branch. Read-only revalidation remains lawful.

REVERIFY_RESULT: NEXY-BUILD-CONTROL/RESULTS/TASK-DOC-C-ROLE-ENUM-001--C-SOL-20261005-1921-V8-ROLE-REVERIFY.json
REVERIFY_DECISION: No active final-DOC-C path authorizes PUBLIC_USER through RoleSchema; do not delete PUBLIC_USER solely from this requirement.
SEPARATE_ROUTE_GAPS: SYSTEM verify-otac/session-me authority mismatches remain tracked independently and are not closed by this task.
SOURCE_MUTATION: NONE
PROTECTED_UPSTREAM_MUTATION: NONE
