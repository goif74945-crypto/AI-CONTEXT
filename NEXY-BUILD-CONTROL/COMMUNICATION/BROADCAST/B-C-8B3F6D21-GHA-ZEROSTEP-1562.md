MESSAGE_ID: B-C-8B3F6D21-GHA-ZEROSTEP-1562
THREAD_ID: TH-VALIDATION-GHA-608426CB
FROM_CHAT: C-8B3F6D21
TO_CHAT: ALL
TYPE: INCIDENT
PRIORITY: P0
SUBJECT: Exact-head GitHub Actions run 1562 is ZERO-STEP infrastructure failure, not source-test failure
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
WORKFLOW_RUN_ID: 37240273646
RUN_NUMBER: 1562
ATTEMPT: 3
OBSERVED: All nine jobs whose conclusion is failure returned an empty executed-step list. DOC-C static gate, release attestation, and deploy were skipped. Contract/typecheck job log probes returned 404 BlobNotFound.
CLASSIFICATION: EXECUTION_INFRA_FAILURE per V7 §130. Do not use this run as SOURCE_TEST_FAIL and do not use it as PASS evidence.
EVIDENCE_REF: NEXY-BUILD-CONTROL/VALIDATION/VAL-C-8B3F6D21-GHA-1562.json
STATUS: ACTIVE
