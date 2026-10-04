TASK_ID: T-EC2F32C6
CREATOR_CHAT: C-62EAE9D7
OWNER_CHAT: C-62EAE9D7
STATUS: IMPLEMENTING
PRIORITY: P1
RISK: MEDIUM
BASE_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
TARGET_PATHS:
- packages/core/__tests__/**
SEMANTIC_SCOPE: Raise packages/core branch coverage from observed 83.13% to >=90% by adding legitimate behavior tests. Production behavior changes are out of scope unless a real defect is independently proven.
DEPENDENCIES:
- Railway validation build logs for deployment 6ebf2acb-1889-450c-874a-1114b4f51531
BLOCKS:
- NEXY Validation R2 - nexy-validation-branch
TEST_PLAN:
- run targeted core tests
- run npm run test:coverage
- run npm run check:coverage
- verify no assertions weakened or tests skipped
REVIEW_STATE: PENDING
LAST_PROGRESS: Root cause isolated to coverage core branches=83.13%, threshold=90%
NEXT_ACTION: map uncovered branches to source and add tests
