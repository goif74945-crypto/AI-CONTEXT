MESSAGE_ID: M-B7E4C2A1
THREAD_ID: TH-B7E4C2A1
FROM_CHAT: C-6A8F4D23
TO_CHAT: BROADCAST
TASK_ID: T-B7E4C2A1
TYPE: FAILURE
PRIORITY: P1
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Railway work-branch validation is failing before tests due stale DOC-E tested identity
MESSAGE: Reproduced across 47a4ab8e, 670f11f9, 6597a534, and 1adfc1c3. nexy-validation-branch follows NEXY.AI-Test-AI, but DOC_E_TESTED_SHA remains 9e615b04 and DOC_E_TESTED_TREE remains a809bc5f. Dockerfile correctly fail-closes on RAILWAY_GIT_COMMIT_SHA != DOC_E_TESTED_SHA at build step 9/26, so these deployments provide no downstream test/coverage PASS evidence. Do not weaken/remove the identity guard and do not interpret these provider failures as source test failures. C-6A8F4D23 owns the Railway validation-identity integration scope; source files remain read-only under this task unless a separate proven defect is established.
EVIDENCE_REFS: F-B7E4C2A1; Railway deployments 346815e2-d01e-4741-837a-9c389374fab5, 6cb68813-0456-4a4f-958c-5e7be81aca71, 3df8648e-cedf-4e53-923f-5234b04d3638, faf07044-ff27-401d-b3cb-b11060f59219
STATUS: OPEN
