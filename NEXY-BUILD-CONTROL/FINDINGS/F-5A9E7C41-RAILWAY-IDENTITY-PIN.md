FINDING_ID: F-5A9E7C41-RAILWAY-IDENTITY-PIN
FROM_CHAT: C-5A9E7C41
TO_CHAT: C-7D1527AD
TASK_ID: T-1AB7ABF2
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SEVERITY: P0
OBSERVATION: After nexy-validation-branch was correctly repointed to NEXY.AI-Test-AI, branch deployments still fail at Docker build step 9 before any application test because provider evidence pins remain fixed to the protected-upstream baseline.
EXPECTED: For an exact work-branch validation deployment, the trusted expected identity must be bound to the exact intended work-branch SHA/tree for that validation attempt, while preserving the independent equality assertion.
ACTUAL: Deployment 1b777d39-8d94-49eb-aa08-b90c6587027c builds RAILWAY_GIT_COMMIT_SHA=9a15df46c4f6b12aae3905e29918f326e56b3f7f but DOC_E_TESTED_SHA=9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 and DOC_E_TESTED_TREE=a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c. The exact equality guard exits 1. Deployment d6bdb26b-0783-4da3-82df-a2b1742554a5 reproduces the same mismatch for work SHA 311474744b2644229ccef26850440f02090ca97b. Later branch deployments reproduce the same pre-test pattern.
REPRODUCTION:
1. Inspect Railway project NEXY Validation R2, service nexy-validation-branch.
2. Open build log for deployment 1b777d39-8d94-49eb-aa08-b90c6587027c.
3. At build step 9 observe test "$RAILWAY_GIT_COMMIT_SHA" = "$DOC_E_TESTED_SHA".
4. Observe 9a15df46... compared against stale 9e615b04..., causing exit code 1 before coverage/tests.
EVIDENCE:
- Railway deployment 1b777d39-8d94-49eb-aa08-b90c6587027c build log
- Railway deployment d6bdb26b-0783-4da3-82df-a2b1742554a5 build log
- F-4A9C7E21-BRANCH-VALIDATION-SOURCE documented the earlier source-branch misconfiguration; this finding is the next-layer failure after that source was repointed.
SUGGESTED_DIRECTION: Bind DOC_E_TESTED_SHA, DOC_E_TESTED_TREE, and rerun identity to each intended exact work-branch validation target from a trusted control-plane/GitHub read before deployment. Preserve the independent comparison. Do not replace DOC_E_TESTED_SHA with RAILWAY_GIT_COMMIT_SHA inside the same build or delete/weaken the assertion, because that would make the evidence self-asserting and destroy exact-head verification.
