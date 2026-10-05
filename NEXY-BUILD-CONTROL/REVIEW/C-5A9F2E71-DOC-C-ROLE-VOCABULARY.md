# DOC-C role vocabulary review

CHAT_ID: C-5A9F2E71
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: REPRODUCED_CONTRACT_DRIFT
CANONICAL_REQUIREMENT_RECORD: NOT_CREATED_TOOL_GATE

FACT:
- Final DOC-C storage enum lists Role = OWNER | OPERATOR | AUDITOR | SYSTEM.
- prisma/schema.prisma at blob 0c557a1bb9b02859bb479655575c3566e201eb6f contains exactly those four Role variants.
- packages/contracts/envelope.ts at blob daf1156b3431150e667b5e18727d8abe9bdc9b75 has RoleSchema with an additional PUBLIC_USER value.
- tests/integration/directives/read-auth.spec.ts at blob 560bc7a5bdc99211395faf5fd46c826e6312fd5e treats PUBLIC_USER as a denied role.
- Therefore wire-contract role validation is broader than both final DOC-C and storage/auth behavior.

IMPACT:
A consumer can validate PUBLIC_USER as an envelope actor role even though the canonical application/storage role set does not contain it. This is a contract parity defect at the reviewed SHA.

NEXT SAFE REPAIR AFTER SOURCE MUTATION UNBLOCKS:
Constrain RoleSchema to the four final DOC-C roles, add a contract assertion for the exact role set, then run envelope and directive authorization tests at the exact worker SHA.

GLOBAL_BLOCKER:
INCIDENT-WORKER-REF-PREFIX-COLLISION-001 prevents compliant worker-branch source mutation.
