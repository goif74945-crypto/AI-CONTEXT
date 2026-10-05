TASK_ID: TASK-QUEUE-RETRY-CAP-001
OWNER_CHAT: C-SOL-20261006-0143-QUEUE-RETRY-CAP
STATUS: IMPLEMENTING
PRIORITY: P1
BASE_SHA: cf2da83c1a56fedbdb8812e4d2664d39ce7cc8cc
BASE_BRANCH: NEXY.AI-Test-AI
WORKER_BRANCH: NEXY.AI-Test-AI-work-queue-retry-cap-6c8f21a4
SEMANTIC_SCOPE: DOC-C queue max-concurrent invariant on explicitly authorized retry of an existing failed BullMQ job.
TARGET_PATHS:
- packages/queue/jobs.ts
- tests/contract/queue-retry-cap.test.ts
REQUIREMENT: max_concurrent_pipeline_runs = 10 must apply to both new enqueue and failed-job retry; no automatic retry widening.
OVERLAP_CHECK: TASK-QUEUE-FAILED-STATE-CAS-001 targets packages/queue/dispatch.ts and its CAS test; no target-path overlap.
PROTECTED_SCOPE:
- NEXY.ai
- packages/queue/dispatch.ts
- auth
- FSM/state matrix
- Vault
MUTATION_BOUNDARY: Check capacity before existing.failed.retry(); preserve idempotent hits and retry authorization semantics; add focused regression only.
