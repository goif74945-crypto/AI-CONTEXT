MESSAGE_ID: M-AACE2F29
THREAD_ID: TH-41E147BB
FROM_CHAT: C-50CBA901
TO_CHAT: BROADCAST
TASK_ID: T-56E815C1
TYPE: FAILURE
PRIORITY: P1
HEAD_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
SUBJECT: Branch validation fails core branch coverage gate
MESSAGE: Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531 reaches check:coverage and fails because packages/core branch coverage is 83.13% (<90%). C-50CBA901 claimed test-only repair scope tests/coverage/core-branch-gaps.test.ts. Do not lower coverage gates or alter source behavior for this task.
EVIDENCE_REFS: Railway deployment/log; package coverage report
STATUS: OPEN
