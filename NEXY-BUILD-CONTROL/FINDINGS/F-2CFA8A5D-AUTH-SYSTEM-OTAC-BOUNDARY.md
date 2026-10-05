FINDING_ID: F-2CFA8A5D-AUTH-SYSTEM-OTAC-BOUNDARY
TYPE: AUTHORITY_BOUNDARY_DEFECT / CONTRACT_DRIFT / UNHANDLED_REQUIRED_STATE
SEVERITY: P1
STATUS: DUPLICATE_SUPERSEDED
REVIEWER_CHAT: C-2CFA8A5D
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
REQ_ID: REQ-DOC-C-4-2-AUTH-VERIFY-SUCCESS-WIRE-001

SPEC_EVIDENCE:
- Final DOC-C paragraphs 10071-10105 define POST /api/auth/verify-otac.
- Successful response role is explicitly constrained to "OWNER" | "OPERATOR" | "AUDITOR".
- Final DOC-C paragraphs 10269-10301 define POST /api/vault/commit RBAC as OWNER / SYSTEM, proving SYSTEM is a distinct required authority in the same active build spec.

SOURCE_EVIDENCE:
- prisma/schema.prisma@608426cb Role enum includes OWNER, OPERATOR, AUDITOR, SYSTEM; Session.role and User.role use that enum.
- packages/api/auth.ts@608426cb resolves role directly as userRecord?.role ?? Role.AUDITOR and creates a session with that role. There is no pre-success guard rejecting Role.SYSTEM.
- The same handler emits response data role directly, so an existing durable SYSTEM user can produce HTTP 200 verify-otac data with role="SYSTEM", outside the explicit final-DOC-C success union.
- packages/validation/api.schema.ts ManageUserRoleBodySchema allows only OWNER/OPERATOR/AUDITOR, showing human owner role management intentionally does not provision SYSTEM.
- tests/coverage/auth-decision-paths.test.ts rejects SYSTEM for human logout but contains no verify-otac SYSTEM-role guard.
- tests/contract/canonical-api.test.ts explicitly verifies SYSTEM authority for vault commit, including cross-user ownership bypass required by the SYSTEM service role.

OBSERVED:
Human OTAC authentication and SYSTEM service authority are not separated at verify-otac. A legitimate persisted SYSTEM role is accepted into the human login success path and can escape through a response role value the final DOC-C route does not permit.

EXPECTED:
The human verify-otac success path must never produce a role outside OWNER/OPERATOR/AUDITOR, while required SYSTEM vault authority must remain available through an explicitly authorized service/system boundary.

ASSUMPTION:
None for the mismatch itself. The exact repair/error mapping is not inferred here.

UNKNOWN:
The final DOC-C route does not explicitly state which listed verify-otac error should represent a SYSTEM principal attempting human OTAC authentication. Repair design must choose an authority-safe fail-closed mapping or locate a separate active clause.

BLOCKER:
INC-BRANCH-NAMESPACE-001 prevents Constitution-compliant source mutation.

VERDICT:
DUPLICATE of canonical finding FINDING-DOC-C-ROLE-SYSTEM-SESSION-AUTHORITY-001, which predates this record and covers the broader verify-otac + session/me boundary. Do not create separate work from this duplicate record. Preserve it only as corroborating independent evidence.
