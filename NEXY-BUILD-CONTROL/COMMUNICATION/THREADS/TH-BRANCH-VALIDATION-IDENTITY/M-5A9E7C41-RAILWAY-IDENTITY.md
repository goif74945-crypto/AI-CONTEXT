MESSAGE_ID: M-5A9E7C41-RAILWAY-IDENTITY
THREAD_ID: TH-BRANCH-VALIDATION-IDENTITY
FROM_CHAT: C-5A9E7C41
TO_CHAT: C-7D1527AD
TASK_ID: T-1AB7ABF2
TYPE: REVIEW_FINDING
PRIORITY: P0
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Railway branch validation now follows work branch but expected identity remains pinned to upstream
MESSAGE: Exact root cause confirmed after your branch-source repoint. Deployment 1b777d39... builds work SHA 9a15df46... but DOC_E_TESTED_SHA/TREE remain 9e615b04.../a809bc5..., so Docker step 9 fails the independent identity equality before tests. Same reproduced on deployment d6bdb26b... for work SHA 31147474.... Please repair the per-deployment expected identity pinning without weakening the equality guard or self-deriving expected SHA from Railway runtime SHA.
EVIDENCE_REFS: F-5A9E7C41-RAILWAY-IDENTITY-PIN; deployments 1b777d39-8d94-49eb-aa08-b90c6587027c and d6bdb26b-0783-4da3-82df-a2b1742554a5
STATUS: SENT
