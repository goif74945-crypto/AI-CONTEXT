FINDING_ID: F-0DC2D7E4-03
TYPE: REQUIREMENT_AUTHORITY_MISCLASSIFICATION
SEVERITY: P0_CONTROL
STATUS: OPEN
REQ_ID: REQ-G22-STATIC-RCS
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

OBSERVED:
REQ-G22-STATIC-RCS classifies G22 paragraphs 7702-7739 and related G20/G21 material as DOC-C BUILD SPEC.

PRIMARY_SOURCE:
- G20/G21/G22 occur before NEXY — EXECUTION PACK vNEXT.1 and before FINAL VERDICT.
- FINAL VERDICT is raw paragraph 9834.
- Build obligation comes from DOC-C only at 9844.
- Final DOC-C is raw paragraphs 9886..10499.
- Final DOC-C contains no G20, G21, G22, CapabilityNode, MaxDepth, permission_scope, or static RCS material.

SOURCE_SCOPE:
- config/experimental-scope.ts classifies packages/phase-f/** as experimental and explicitly lists capability-node.spec.ts in experimental tests.
- root tsconfig excludes packages/phase-f/**.

RESULT:
G22 may be historical/experimental design evidence, but REQ-G22-STATIC-RCS is not verified as an active DOC-C build requirement at this spec hash.

ACTION:
Mark this requirement authority REVERIFY_REQUIRED / EXPERIMENTAL unless a final-DOC-C incorporation clause is produced. Do not schedule it as required P0/P1 build work.

SOURCE_MUTATION: NONE
