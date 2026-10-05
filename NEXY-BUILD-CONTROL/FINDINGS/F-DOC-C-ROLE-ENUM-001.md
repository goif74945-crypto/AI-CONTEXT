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
STATUS: SUPERSEDED_AUTHORITY_MISCLASSIFICATION

SUPERSEDED_BY_AUTHORITY_CORRECTION: NEXY-BUILD-CONTROL/FINDINGS/F-0DC2D7E4-04-ROLE-AUTHORITY.md
SUPERSESSION_REVIEW: NEXY-BUILD-CONTROL/REVIEW/C-5A9F2E71-DOC-C-ROLE-VOCABULARY--SUPERSEDED-BY-C-SOL-20261005-1921.json
FINAL_REVERIFY_RESULT: NEXY-BUILD-CONTROL/RESULTS/TASK-DOC-C-ROLE-ENUM-001--C-SOL-20261005-1921-V8-ROLE-REVERIFY.json
RESOLUTION: Do not treat PUBLIC_USER membership in shared RoleSchema as a final-DOC-C defect without a concrete route-local authorization violation. Separate SYSTEM session authority gaps remain open.
