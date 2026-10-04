FINDING_ID: F-4A9C7E21-BRANCH-VALIDATION-SOURCE
FROM_CHAT: C-4A9C7E21
TO_CHAT: C-7D1527AD; C-7B5E20D1
TASK_ID: T-1AB7ABF2; T-7B5E20D1
HEAD_SHA: cf2f5e44032de0b241f4068b5ff919bf1499a800
SEVERITY: P1
OBSERVATION: Railway service "nexy-validation-branch" is currently connected to repo goif74945-crypto/NEXY.AI- branch NEXY.ai, not NEXY.AI-Test-AI.
EXPECTED: branch validation for the V4 work stream must execute the exact NEXY.AI-Test-AI revision being claimed.
ACTUAL: latest Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531 validates upstream SHA 9e615b04 on NEXY.ai; work branch is now cf2f5e44 and 10 commits ahead.
REPRODUCTION: Railway describe_service project 01537473-6a6d-42a0-856f-40d8a4e6a712 service 3c290782-e2f0-4e5b-87d9-58bae4d4dba8 environment 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8.
EVIDENCE: Railway source.branch=NEXY.ai; GitHub compare NEXY.ai...NEXY.AI-Test-AI ahead_by=10.
SUGGESTED_DIRECTION: establish exact-head validation for NEXY.AI-Test-AI without changing protected NEXY.ai. Do not treat upstream Railway results as PASS evidence for work-branch commits.
