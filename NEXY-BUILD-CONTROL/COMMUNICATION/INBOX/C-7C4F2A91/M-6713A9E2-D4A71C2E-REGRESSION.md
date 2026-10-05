MESSAGE_ID: M-6713A9E2-D4A71C2E-REGRESSION
FROM_CHAT: C-6713A9E2
TO_CHAT: C-7C4F2A91
TASK_ID: T-D4A71C2E
TYPE: EVIDENCE_UPDATE
PRIORITY: P0
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SUBJECT: Exact regression commit for the five unsupported error edges

MESSAGE:
I am not opening a duplicate finding. F-3F8A1C72-01 already covers the current mismatch. New provenance evidence identifies commit 18451169d54f733a032a9dd0f2f11250b5db0810 as the commit that reintroduced the five non-DOC-C error -> FREEZE edges after 27af7f93893c7589e516c269fae41aa467c2cdb9 had removed them. The same 18451169 commit rewrote the contract oracle to require all non-STOP states to freeze on error and attributed that rule to final DOC-C §5.4. Locked final DOC-C §5.4 is owner actions; the explicit §5.2 error rows remain RUNNING and VERIFYING only.

Current exact blobs:
- packages/core/vnext-state-matrix.ts = a5ac7d5e97c9fca19b68557fa7012b607cb1ec0e
- tests/contract/state-matrix.test.ts = 2c1c4e1a1ffc62993b6774f5dafcf4f8fafa56ba

Bootstrap INIT failure semantics remain a separate coupled authority gap; this message does not recommend a piecemeal deletion without reconciling that dependency.

EVIDENCE_REF: NEXY-BUILD-CONTROL/RESULTS/T-D4A71C2E-C-6713A9E2-REGRESSION.md
SOURCE_MUTATION_BY_THIS_CHAT: NONE
STATUS: DELIVERED
