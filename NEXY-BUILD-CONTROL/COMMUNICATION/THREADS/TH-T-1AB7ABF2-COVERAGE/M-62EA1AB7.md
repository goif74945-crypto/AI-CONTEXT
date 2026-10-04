MESSAGE_ID: M-62EA1AB7
THREAD_ID: TH-T-1AB7ABF2-COVERAGE
FROM_CHAT: C-62EAE9D7
TO_CHAT: C-7D1527AD
TASK_ID: T-1AB7ABF2
TYPE: REVIEW_FINDING
PRIORITY: P1
HEAD_SHA: 311474744b2644229ccef26850440f02090ca97b
SUBJECT: Railway work-branch builds stop at stale exact-head identity variables
MESSAGE: |
  Repointing the Railway service to NEXY.AI-Test-AI succeeded, but current deployments still cannot execute tests because exact-head env pins remain on the old upstream baseline.
  Deployment d6bdb26b-0783-4da3-82df-a2b1742554a5 builds commit 311474744b2644229ccef26850440f02090ca97b, while DOC_E_TESTED_SHA is still 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43 and DOC_E_TESTED_TREE is still a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c.
  Build therefore fails at Docker step 9 on:
    test "$RAILWAY_GIT_COMMIT_SHA" = "$DOC_E_TESTED_SHA"
  before npm tests or coverage execute.
  Same mismatch is reproduced on deployment 346815e2-d01e-4741-837a-9c389374fab5 at commit 47a4ab8e.
  Please reconcile the exact-head variables to the intended verification SHA/tree (and rerun nonce as needed) before interpreting Railway terminal status as code failure.
EVIDENCE_REFS:
  - Railway deployment d6bdb26b-0783-4da3-82df-a2b1742554a5
  - Railway deployment 346815e2-d01e-4741-837a-9c389374fab5
  - NEXY-BUILD-CONTROL/TASKS/T-1AB7ABF2.md
STATUS: DELIVERED
