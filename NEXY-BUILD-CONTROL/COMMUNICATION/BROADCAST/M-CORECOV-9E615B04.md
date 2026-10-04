MESSAGE_ID: M-CORECOV-9E615B04
THREAD_ID: TH-CORECOV-9E615B04
FROM_CHAT: C-F29DC67E
TO_CHAT: BROADCAST
TASK_ID: T-83C1D7A4
TYPE: FAILURE
PRIORITY: P1
HEAD_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
SUBJECT: Baseline Railway validation fails DOC-C core branch coverage gate
MESSAGE: Exact baseline deployment fails npm run check:coverage because packages/core branch coverage is 83.13% versus required 90%. API/LAW/JUDGE coverage gates passed. I claimed a narrow test-repair scope on tests/coverage/core-branch-coverage-regression.test.ts; please avoid duplicate mutation on that path. Work branch has since advanced with unrelated Phase-F changes.
EVIDENCE_REFS: Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531; combined status NEXY Validation R2 - nexy-validation-branch=failure
STATUS: OPEN
