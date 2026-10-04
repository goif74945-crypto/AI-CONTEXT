FAILURE_ID: F-7AC3E7D1
TASK_ID: T-EC2F32C6
REPORTER_CHAT: C-62EAE9D7
NEXY_BRANCH: NEXY.AI-Test-AI
NEXY_HEAD_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
STATUS: ACTIVE_REPAIR
FAILURE_CLASS: BUILD_IMAGE_VALIDATION
SERVICE: NEXY Validation R2 - nexy-validation-branch
RAILWAY_PROJECT_ID: 01537473-6a6d-42a0-856f-40d8a4e6a712
RAILWAY_DEPLOYMENT_ID: 6ebf2acb-1889-450c-874a-1114b4f51531
OBSERVED:
- npm run test:coverage completed
- coverage api PASS
- coverage law PASS
- coverage judge PASS
- coverage core FAIL
- core metrics: lines=93.88%, statements=92.41%, functions=95.65%, branches=83.13%
- required core threshold: 90% under every standard metric
FAILURE_COMMAND: npm run check:coverage
FAILURE_EXIT_CODE: 1
NEXT_ACTION: add legitimate branch tests for packages/core without weakening thresholds or assertions
