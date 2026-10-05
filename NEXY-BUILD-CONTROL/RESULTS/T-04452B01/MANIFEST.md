TASK_ID: T-04452B01
STATUS: CANDIDATE_PREPARED_NON_MUTATING
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_COMMIT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_FILE_BLOB_SHA: 25d26bf233b1d7b446027aad391688b7e91b09a0
TEST_FILE_BLOB_SHA: a04597422ebfa57f2bff8e7d72885e361b492b9b
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
CANDIDATE_SOURCE_CONTROL_COMMIT: 34c29bd63d3b49081b58182185232a2b7423e249
CANDIDATE_TEST_CONTROL_COMMIT: 8c739bc4d41ffc8889ac950bf6e18c16e908c1be
SEMANTIC_RULE:
- canonical G22 R001-R010 identities are pinned exactly
- authority escalation emits R002_PERMISSION_ESCALATION
- R007 remains R007_NONDET_SYSCALL and is not repurposed
- invalid-node/schema failures map to R008_SCHEMA_NONCANONICAL
- non-G22 legacy conditions keep rejection behavior but use INTERNAL_* identities
- results are deduplicated and sorted with compareCanonicalText
SOURCE_MUTATION: NONE

CANDIDATE_REVISION:
- source control commit: 45b272b1d16c0b3df19868c8757ac47d86f12510
- test control commit: 68409b5d6ab49d3465f3ade953e145cae821253c
- R001-R010 repurposing scan: PASS; only authoritative G22 identities remain under those prefixes
- duplicate-node rejection identity changed to INTERNAL_DUPLICATE_NODE
