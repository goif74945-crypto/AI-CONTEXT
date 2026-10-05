FINDING_ID: F-0DC2D7E4-04
TYPE: REQUIREMENT_AUTHORITY_MISCLASSIFICATION
SEVERITY: P0_CONTROL
STATUS: OPEN
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

OBSERVED:
REQ-DOC-C-ROLE-ENUM-001 cites raw paragraphs 10724-10729 as final DOC-C and concludes Role = OWNER | OPERATOR | AUDITOR | SYSTEM is exact DOC-C build authority.

PRIMARY_SOURCE:
- Final DOC-C begins at raw paragraph 9886.
- DOC-D begins at raw paragraph 10500, so final DOC-C has ended before 10724.
- raw 10723 = 7) STORAGE LAW — MIGRATION-READY PACK.
- raw 10724 = 7.1 Enums.
- raw 10726 = Role = OWNER | OPERATOR | AUDITOR | SYSTEM.
Therefore the exact four-value Role declaration is outside final DOC-C.

WHAT FINAL DOC-C DOES SAY:
- verify-otac/session responses use OWNER | OPERATOR | AUDITOR.
- canonical route RBAC uses OWNER/OPERATOR/AUDITOR and one vault route permits OWNER / SYSTEM.
- PUBLIC_USER is absent from final DOC-C.
These facts do not by themselves prove an exact global four-value Role type.

RESULT:
The exact global Role union is UNKNOWN under final DOC-C unless another primary final-DOC-C clause is found. The current requirement must not drive source deletion/addition as DOC-C authority.

ACTION:
Reclassify/reverify the requirement. Keep route-local final-DOC-C RBAC/response role requirements separate from the non-final storage-law Role enum.

SOURCE_MUTATION: NONE
