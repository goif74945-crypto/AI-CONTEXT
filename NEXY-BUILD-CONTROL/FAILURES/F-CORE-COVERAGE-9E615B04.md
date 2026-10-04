FAILURE_ID: F-CORE-COVERAGE-9E615B04
TASK_ID: T-83C1D7A4
REPORTER_CHAT: C-F29DC67E
STATUS: INVESTIGATING
SEVERITY: P1
TARGET_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
EVIDENCE_CLASS: E1/E2 build-test gate
OBSERVED: Railway deployment 6ebf2acb-1889-450c-874a-1114b4f51531 failed during npm run check:coverage.
ERROR_SIGNATURE: coverage core below 90% for branches: lines=93.88% statements=92.41% functions=95.65% branches=83.13%.
UNAFFECTED_GATES_OBSERVED: API coverage PASS; LAW coverage PASS; JUDGE coverage PASS.
ROOT_CAUSE: NOT_YET_ESTABLISHED; branch-path test coverage gap under packages/core is the current hypothesis.
NEXT_ACTION: inspect per-file coverage and core branch structure, then add real behavior tests.
