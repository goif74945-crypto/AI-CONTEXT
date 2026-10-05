REQ_ID: REQ-DOC-C-3-1-ERROR-CODE
CHAT_ID: C-17A4D82E
TEST_ID: TEST-DOC-C-3-1-ERROR-CODE-CI-01
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
COMMIT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
WORKFLOW_RUN_ID: 37240273646
WORKFLOW_ATTEMPT: 3
JOB: Contract tests
JOB_ID: 111716421766
COMMAND: UNKNOWN_NO_STEPS_MATERIALIZED
RUNNER: GitHub Actions; runner assignment not exposed
RESULT: EXECUTION_INFRA_FAILURE
EXIT_CODE: UNKNOWN_NO_EXECUTED_STEP
EVIDENCE:
- exact-head workflow run concluded failure
- contract-test job concluded failure
- job steps endpoint returned []
- job log fetch returned BlobNotFound
INTERPRETATION:
- not source-test-fail evidence
- requirement remains MATCH, not VERIFIED
- fresh executed exact-SHA test evidence is still required
