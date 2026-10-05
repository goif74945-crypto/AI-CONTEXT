TASK_ID: TASK-DOC-C-ROLE-ENUM-001
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
GOAL: align canonical RoleSchema with final DOC-C and storage role vocabulary.
SCOPE: packages/contracts/envelope.ts; tests/contract/envelope.test.ts; tests/integration/directives/read-auth.spec.ts
ACCEPTANCE: RoleSchema exact set OWNER, OPERATOR, AUDITOR, SYSTEM; PUBLIC_USER rejected; Prisma remains unchanged unless new primary evidence requires a change; affected tests execute at exact worker SHA.
EVIDENCE_TARGET: source diff; exact RoleSchema assertion; envelope contract test; directive authorization test; exact SHA metadata.
PRIORITY: P1
RISK: HIGH
STATUS: BLOCKED
OWNER: UNASSIGNED
MUTATION_LEASE: NONE
BASE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
BLOCKER: INCIDENT-WORKER-REF-PREFIX-COLLISION-001
UNBLOCK_CONDITION: coordinated non-colliding worker isolation mechanism authorized for V7 source mutation.
