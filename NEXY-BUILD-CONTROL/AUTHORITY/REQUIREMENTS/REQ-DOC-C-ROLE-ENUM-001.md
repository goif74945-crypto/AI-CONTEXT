REQ_ID: REQ-DOC-C-ROLE-ENUM-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_PAGE: UNKNOWN_DOCX_PAGE_MAP
SPEC_LINES: FINAL VERDICT 9834-9845; final DOC-C 9886-10499; role-bearing clauses 10094-10098, 10112-10127, 10269-10282; non-DOC-C storage enum 10723-10729
SPEC_TEXT: Final DOC-C defines route-local role contracts: verify-otac and session/me expose OWNER | OPERATOR | AUDITOR; vault commit authorizes OWNER / SYSTEM. The exact global declaration Role = OWNER | OPERATOR | AUDITOR | SYSTEM occurs outside final DOC-C after DOC-D begins and is not DOC-C build authority.
AUTHORITY_CLASS: DOC-C BUILD SPEC FINAL — ROUTE_LOCAL_ROLE_CONTRACTS; GLOBAL_ROLE_UNION_UNKNOWN
EXPECTED_BEHAVIOR:
- POST /api/auth/verify-otac response role is OWNER | OPERATOR | AUDITOR.
- GET /api/session/me requires and returns OWNER | OPERATOR | AUDITOR.
- POST /api/vault/commit authorizes OWNER / SYSTEM.
- Route-local authorization must not grant PUBLIC_USER authority where final DOC-C enumerates only active roles.
FORBIDDEN_BEHAVIOR:
- cite paragraphs 10724-10729 as final DOC-C.
- claim the exact global four-value Role union is explicitly defined by final DOC-C.
- infer that mere schema acceptance of PUBLIC_USER grants public write authority without an active authorization path.
- reintroduce PUBLIC_USER into final-DOC-C protected route RBAC.
AFFECTED_SYSTEMS: API contracts; route RBAC; envelope actor metadata
DEPENDENCIES: final DOC-C route contracts; SystemEnvelope actor metadata
IMPLEMENTATION_PATHS: packages/contracts/envelope.ts; route-specific auth modules
TEST_PATHS: tests/contract/envelope.test.ts; tests/integration/directives/read-auth.spec.ts; route-specific auth tests
STATUS: REVERIFY_REQUIRED
STATUS_REASON: Current source RoleSchema accepts PUBLIC_USER, but final DOC-C does not declare an exact global Role union. The inspected directive read path explicitly denies PUBLIC_USER. A source mutation is not authorized until an active final-DOC-C path is proven to treat PUBLIC_USER as valid where the route contract forbids it.
LAST_VERIFIED_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
EVIDENCE:
- authoritative DOCX SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
- final DOC-C ends at paragraph 10499; DOC-D begins at 10500.
- exact global Role declaration appears at paragraph 10726 outside final DOC-C.
- packages/contracts/envelope.ts blob daf1156b3431150e667b5e18727d8abe9bdc9b75 includes PUBLIC_USER in RoleSchema.
- tests/integration/directives/read-auth.spec.ts blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e denies PUBLIC_USER on protected directive/run reads.
OPEN_QUESTION: Does any active final-DOC-C runtime path consume RoleSchema directly such that PUBLIC_USER is accepted as an authorized role contrary to a route-local contract? If not, no DOC-C source gap is established by RoleSchema membership alone.
