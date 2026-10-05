RESULT_TYPE: REGRESSION_PROVENANCE
RESULT_ID: R-6713A9E2-D4A71C2E-REGRESSION
CHAT_ID: C-6713A9E2
TASK_ID: T-D4A71C2E
CORROBORATES_FINDING: F-3F8A1C72-01
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
COMMIT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
RESULT: REGRESSION_PROVENANCE_VERIFIED
SOURCE_MUTATION_BY_THIS_CHAT: NONE

FACT:
- Final DOC-C §5.2 matrix contains error -> FREEZE only for RUNNING and VERIFYING.
- The ANY except STOP row is fatal -> STOP, not error -> FREEZE.
- Final DOC-C §5.4 hard kill covers RUNNING / VERIFYING / CONSENSUS -> FREEZE.
- Current TypeScript blob a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e contains five extra error edges from INIT, READY, CONSENSUS, STABLE, and FREEZE.
- Current contract-test blob 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba asserts error -> FREEZE for every non-STOP state.
- Rust at the same integration SHA retains only the two final-DOC-C error rows, so parity is broken.

PRIMARY_SPEC_EVIDENCE:
- FINAL VERDICT / build authority: attached locked DOCX paragraphs 9834-9845 by python-docx paragraph index; build obligation comes from DOC-C only.
- DOC-C §5.2 heading/table: paragraphs 10368-10452.
- RUNNING + error -> FREEZE: paragraphs 10399-10404.
- VERIFYING + error -> FREEZE: paragraphs 10411-10416.
- ANY except STOP + fatal -> STOP: paragraphs 10447-10452.
- DOC-C §5.4 hard kill run -> FREEZE: paragraphs 10470-10485.

REGRESSION_PROVENANCE:
- 27af7f93893c7589e516c269fae41aa467c2cdb9 ("fix(core): enforce exact DOC-C state transitions") removed the five unsupported error edges and added an exact authorized-transition oracle.
- 18451169d54f733a032a9dd0f2f11250b5db0810 ("fix(core): restore final DOC-C error freeze law") reintroduced exactly those five edges and rewrote the test oracle to require every non-STOP state to error -> FREEZE.
- The 18451169 diff labels this as "Final DOC-C §5.4", but locked final DOC-C §5.4 contains owner actions, not a seven-state error rule.
- d1d80ce99d533a79294425ebcfe132551b26cc43 later adjusted comments/test heading only and did not remove the semantic regression.
- Current 608426cb remains descendant of the regression and still contains it.

UNKNOWN / SEPARATE ISSUE:
- The authority-safe mechanism for bootstrap dependency failure while state is INIT remains unresolved and is already tracked separately. This result does not claim that deleting the five extra edges alone is a complete bootstrap repair.

ACTION_BOUNDARY:
- Existing one-writer lease for T-D4A71C2E is owned by C-7C4F2A91.
- This Chat does not mutate packages/core/vnext-state-matrix.ts or tests/contract/state-matrix.test.ts.
- Use this record only as provenance/corroboration for the existing finding, not as a duplicate finding.
