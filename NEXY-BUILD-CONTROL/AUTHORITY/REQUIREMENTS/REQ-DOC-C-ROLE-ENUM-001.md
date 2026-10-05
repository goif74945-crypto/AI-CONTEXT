REQ_ID: REQ-DOC-C-ROLE-ENUM-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_PAGE: UNKNOWN_DOCX_PAGE_MAP
SPEC_LINES: final DOC-C paragraphs 10724-10729; envelope context 9950-10013
SPEC_TEXT: Role = OWNER | OPERATOR | AUDITOR | SYSTEM
AUTHORITY_CLASS: DOC-C BUILD SPEC FINAL
EXPECTED_BEHAVIOR: canonical role vocabulary is exactly OWNER, OPERATOR, AUDITOR, SYSTEM and matches storage.
FORBIDDEN_BEHAVIOR: canonical wire-role validation must not add a role absent from active DOC-C.
AFFECTED_SYSTEMS: API contract, RBAC, storage
DEPENDENCIES: SystemEnvelope actor metadata
IMPLEMENTATION_PATHS: packages/contracts/envelope.ts; prisma/schema.prisma
TEST_PATHS: tests/contract/envelope.test.ts; tests/integration/directives/read-auth.spec.ts
STATUS: MISMATCH
LAST_VERIFIED_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
EVIDENCE: RoleSchema includes PUBLIC_USER at blob daf1156b3431150e667b5e18727d8abe9bdc9b75; Prisma Role has four final DOC-C values at blob 0c557a1bb9b02859bb479655575c3566e201eb6f; read-auth test treats PUBLIC_USER as denied at blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e.
