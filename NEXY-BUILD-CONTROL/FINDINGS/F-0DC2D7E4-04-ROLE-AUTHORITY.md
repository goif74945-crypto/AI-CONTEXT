FINDING_ID: F-0DC2D7E4-04
TYPE: REQUIREMENT_AUTHORITY_MISCLASSIFICATION
SEVERITY: P0_CONTROL
STATUS: RESOLVED_CONTROL_CORRECTION
REQ_ID: REQ-DOC-C-ROLE-ENUM-001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

OBSERVED:
REQ-DOC-C-ROLE-ENUM-001 cited raw paragraphs 10724-10729 as final DOC-C and concluded Role = OWNER | OPERATOR | AUDITOR | SYSTEM was an exact global DOC-C build requirement.

PRIMARY_SOURCE:
- FINAL VERDICT is paragraph 9834.
- DOC-C is the BUILD SPEC at paragraph 9839 and build obligation comes from DOC-C only at 9844.
- final DOC-C runs from 9886 through 10499.
- DOC-D begins at 10500.
- raw 10726 contains Role = OWNER | OPERATOR | AUDITOR | SYSTEM under STORAGE LAW after DOC-D, outside final DOC-C.
- final DOC-C route contracts explicitly use OWNER | OPERATOR | AUDITOR for verify-otac/session and OWNER / SYSTEM for vault commit.

RESOLUTION:
The requirement record was corrected to route-local DOC-C authority and GLOBAL_ROLE_UNION_UNKNOWN. The associated task was changed from an exact four-value mutation task to read-only active-consumer revalidation. No source deletion/addition is authorized by this finding alone.

SOURCE FACT AT 608426cb30398b1f3461866f7079d2a435c96b96:
- RoleSchema includes PUBLIC_USER.
- the inspected protected directive/run read tests explicitly deny PUBLIC_USER.
Therefore RoleSchema membership alone is insufficient evidence of a final-DOC-C authorization defect.

FOLLOW-UP:
TASK-DOC-C-ROLE-ENUM-001 remains REVERIFY_REQUIRED. Open a source repair only if a concrete active final-DOC-C path is proven to authorize PUBLIC_USER contrary to its route contract.

SOURCE_MUTATION: NONE
CONTROL_CORRECTION: APPLIED
