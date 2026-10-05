REVIEW_ID: RV-DOC-C-ROLE-ENUM-CHAT-20261005-GPT56SOL-STATE01
CHAT_ID: CHAT-20261005-GPT56SOL-STATE01
TASK_ID: TASK-DOC-C-ROLE-ENUM-001
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
PHASE: AUTHORITY / BASELINE SHADOW REVIEW
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
FINAL_CANDIDATE_REVIEW: NO
COUNTS_TOWARD_FINAL_REVIEW_COMPLETED: false

FACT — PRIMARY SPEC:
1. FINAL VERDICT says DOC-C = BUILD SPEC and build obligation comes from DOC-C only.
2. Before FINAL VERDICT, historical material explicitly defines Role including PUBLIC_USER (raw paragraphs 8173-8178) and an RBAC matrix including PUBLIC_USER (9278-9288).
3. Final DOC-C begins at raw paragraph 9886 and ends when DOC-D begins at 10500.
4. Within final DOC-C, OTAC/session responses expose human role as OWNER | OPERATOR | AUDITOR (10094-10098 and 10120-10127).
5. Final DOC-C vault commit RBAC explicitly allows OWNER / SYSTEM (10269-10282), proving SYSTEM remains an active DOC-C authorization identity.
6. No explicit canonical Role enum declaration was found inside final DOC-C 9886-10499.
7. The exact declaration “Role = OWNER | OPERATOR | AUDITOR | SYSTEM” appears at raw paragraph 10726 under “7) STORAGE LAW — MIGRATION-READY PACK”, after “6) DOC-D — FINAL PRODUCT DESIGN PACK” begins at 10500. It therefore must not be cited as DOC-C build authority merely by adjacency.

FACT — SOURCE @ EXACT HEAD:
- packages/contracts/envelope.ts blob daf1156b3431150e667b5e18727d8abe9bdc9b75 accepts OWNER, OPERATOR, AUDITOR, SYSTEM, PUBLIC_USER.
- prisma/schema.prisma blob 0c557a1bb9b02859bb479655575c3566e201eb6f stores only OWNER, OPERATOR, AUDITOR, SYSTEM.
- tests/integration/directives/read-auth.spec.ts blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e explicitly denies PUBLIC_USER (along with SYSTEM/INVALID) on human directive read routes.

AUTHORITY RESULT:
- The current REQ record’s claim that “final DOC-C paragraphs 10724-10729” explicitly defines the exact four-value Role enum is AUTHORITY-MISCLASSIFIED.
- The implementation evidence still strongly indicates PUBLIC_USER is historical drift: it is explicit in pre-FINAL material, absent from final DOC-C role-bearing route contracts, and unsupported by storage.
- However, absence is not the same as an explicit DOC-C exact-enum declaration. The requirement should be rewritten around the narrower, provable build obligation: canonical wire/session role handling must not reintroduce historical PUBLIC_USER where final DOC-C contracts enumerate only active identities; SYSTEM support must be tied to the final DOC-C routes that explicitly authorize it.

ENGINEERING INFERENCE:
Removing PUBLIC_USER from RoleSchema is likely the smallest parity repair, but the exact global RoleSchema set should be justified from final DOC-C role-bearing contracts rather than from DOC-D storage law.

REVIEW RESULT:
AUTHORITY_BASIS_FAIL / SOURCE_DRIFT_REPRODUCED.
Do not implement from the current misclassified authority record unchanged. Correct the requirement evidence first, then preserve the candidate repair if the corrected requirement still supports it.

SOURCE MUTATION:
NONE. Global V7 worker-ref namespace TRUE_BLOCK remains active.
