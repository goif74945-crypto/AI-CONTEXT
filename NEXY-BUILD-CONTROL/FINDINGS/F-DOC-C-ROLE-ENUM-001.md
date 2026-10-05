FINDING_ID: F-DOC-C-ROLE-ENUM-001
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
TASK_ID: UNASSIGNED
FROM: C-5A9F2E71
TO: API_CONTRACT / AUTH
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P1
OBSERVED: packages/contracts/envelope.ts RoleSchema accepts PUBLIC_USER while final DOC-C and prisma/schema.prisma define only OWNER, OPERATOR, AUDITOR, SYSTEM. tests/integration/directives/read-auth.spec.ts treats PUBLIC_USER as denied.
EXPECTED: one canonical four-value Role vocabulary across wire contract, storage, and authorization behavior.
SPEC_EVIDENCE: final DOC-C paragraphs 10724-10729, spec hash b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
REPRODUCTION: inspect envelope blob daf1156b3431150e667b5e18727d8abe9bdc9b75, Prisma blob 0c557a1bb9b02859bb479655575c3566e201eb6f, and read-auth test blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e at Test-AI SHA 608426cb30398b1f3461866f7079d2a435c96b96.
STATUS: REPRODUCED
