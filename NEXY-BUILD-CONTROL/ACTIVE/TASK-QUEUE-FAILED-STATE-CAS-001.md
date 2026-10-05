TASK_ID: TASK-QUEUE-FAILED-STATE-CAS-001
OWNER_CHAT: C-SOL-20261006-0143-QUEUE-CAS
STATUS: IMPLEMENTING
PRIORITY: P1
BASE_SHA: c2b99fc456d0babda4dfd88115544cb142969729
WORKER_BRANCH: NEXY.AI-Test-AI/work/queue-failed-state-cas-001
SEMANTIC_SCOPE: durable queue reconciliation CAS; FAILED/CANCELLED/COMPLETED must win stale reconciliation
TARGET_PATHS:
- packages/queue/dispatch.ts
- tests/contract/dispatch-reconciliation-cas.test.ts
