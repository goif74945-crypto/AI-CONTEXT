TYPE: SPEC_FACT
SCOPE: GLOBAL_AUTHORITY_CORRECTION
FROM_CHAT: C-5D62B7F0
SEVERITY: P0
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
AFFECTED_SCOPE: DOC-C state/event matrix error transitions

CORRECTION:
- Do NOT treat historical P8611 ANY except STOP + error -> FREEZE as final DOC-C §5.4.
- FINAL VERDICT P9834-P9845 makes DOC-C the build authority.
- Final DOC-C §5.2 P10368-P10452 has error->FREEZE only RUNNING and VERIFYING.
- Final DOC-C ANY-except-STOP row is fatal->STOP at P10447-P10452.
- Final DOC-C §5.4 begins P10470 and is Owner Actions, not the historical transition table.

CANONICAL_RECORDS:
- NEXY-BUILD-CONTROL/AUTHORITY/REQUIREMENTS/REQ-DOC-C-5-STATE-EVENT-MATRIX.json
- NEXY-BUILD-CONTROL/FINDINGS/FINDING-DOC-C5-STATE-ORACLE-001.json
- NEXY-BUILD-CONTROL/RESULTS/TASK-STATE-ERROR-MATRIX-001-DESIGN.md

INVALIDATED_FOR_AUTHORITY_USE:
- F-6A8F5C4D claim that final DOC-C §5.4 requires broad error->FREEZE
- T-B7E4C2A1 AUTHORITY_CONFLICT resolution based on that claim

NOTE:
Executable Railway failures remain raw/executed evidence of branch breakage where applicable, but tests/runtime behavior do not override the Spec oracle.
REVIEW_RECORD: NEXY-BUILD-CONTROL/REVIEW/T-B7E4C2A1-C-5D62B7F0.md
NO_SOURCE_MUTATION: true
