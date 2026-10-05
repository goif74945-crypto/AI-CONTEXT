TASK_ID: TASK-DOC-C2-3-QUEUE-FUTURE-TSA-001
OWNER_CHAT: C-SOL-20261006-QUEUE-FUTURE-TSA
STATUS: IMPLEMENTING
PRIORITY: P1
BASE_SHA: c1f94b2c59b787a7761079362a82aefbbfca9855
WORKER_BRANCH: NEXY.AI-Test-AI-work-queue-future-tsa-4f2a91c7
SEMANTIC_SCOPE: reject BullMQ enqueuedAt later than authoritative TSA batch time before durable dispatch claim/state/SWARM
TARGET_PATHS:
- packages/queue/payload.ts
- tests/contract/queue-payload.test.ts
- tests/integration/queue-boundary.spec.ts
MUTATION_LEASE: ACTIVE
OVERLAP: none with active queue writers on dispatch.ts/jobs.ts
FORBIDDEN: NEXY.ai; host-clock authority; TTL semantic widening; dispatch/jobs mutation
