TASK_ID: T-DOC-C4-DIR-IDEM-RACE-0144
OWNER_CHAT: C-SOL-20261006-0144-DIR-IDEM
STATUS: TESTING_BLOCKED_INFRA
PRIORITY: P1
BASE_SHA: 1ab5de28aa9f9b5a1a6722dc1e2a20d8b807a87c
WORKER_BRANCH: work/NEXY-AI-Test-AI-directive-idempotency-race-0144
TARGET_PATHS:
- packages/api/directives.ts
- tests/coverage/directive-create-branches.test.ts
SEMANTIC_SCOPE: concurrent same-session same-payload directive idempotency P2002 convergence only
NOTE: NEXY.AI-Test-AI/work/* ref namespace conflicts with existing integration ref; isolated work/* ref used.
BLOCKER: GitHub Actions run 37359827306 attempts 1-2 completed failure before first step (steps=null); Desktop Commander device offline. Source integration remains frozen.
CONTINUATION_REQUIRED: true
