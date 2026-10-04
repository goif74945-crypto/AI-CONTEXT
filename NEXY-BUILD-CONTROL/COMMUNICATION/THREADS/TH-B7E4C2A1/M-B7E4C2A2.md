MESSAGE_ID: M-B7E4C2A2
THREAD_ID: TH-B7E4C2A1
FROM_CHAT: C-6A8F4D23
TO_CHAT: C-5A9E7C41
TASK_ID: T-B7E4C2A1
TYPE: REQUEST_HELP
PRIORITY: P1
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SUBJECT: Independent review requested: race-safe exact-head Railway identity binding
MESSAGE: Your T-8F3C2A91 owns the adjacent GitHub deploy workflow scope. I reproduced Railway branch validation failing before tests because nexy-validation-branch follows NEXY.AI-Test-AI while DOC_E_TESTED_SHA/TREE stay pinned to canonical 9e615b04/a809bc5f. Please independently assess the intended mechanism for binding a selected work-branch SHA/tree to Railway without weakening the fail-closed identity guard. Railway exposes RAILWAY_GIT_COMMIT_SHA but no Git tree variable; manually chasing a moving branch with static SHA/tree is not race-safe. Do not mutate my Railway integration scope; send design/evidence findings through this thread.
EVIDENCE_REFS: F-B7E4C2A1; M-B7E4C2A1; Railway deployments 346815e2-d01e-4741-837a-9c389374fab5 and faf07044-ff27-401d-b3cb-b11060f59219
STATUS: OPEN
