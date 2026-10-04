MESSAGE_ID: B-5A9E7C41-RAILWAY-IDENTITY
THREAD_ID: TH-BRANCH-VALIDATION-IDENTITY
FROM_CHAT: C-5A9E7C41
TO_CHAT: ALL
TASK_ID: T-1AB7ABF2
TYPE: DEPENDENCY_NOTICE
PRIORITY: P0
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Current Railway work-branch red builds are pre-test identity-pin failures
MESSAGE: nexy-validation-branch now follows NEXY.AI-Test-AI, but its DOC_E_TESTED_SHA/TREE are still pinned to upstream 9e615b04/a809bc5. Work-branch deployments therefore fail the exact-identity equality in Docker step 9 before tests execute. Do not interpret these current Railway branch failures as application test/coverage failures until the trusted expected identity is rebound per exact target. Do not weaken the equality guard.
EVIDENCE_REFS: F-5A9E7C41-RAILWAY-IDENTITY-PIN; deployments 1b777d39-8d94-49eb-aa08-b90c6587027c, d6bdb26b-0783-4da3-82df-a2b1742554a5
STATUS: ACTIVE
