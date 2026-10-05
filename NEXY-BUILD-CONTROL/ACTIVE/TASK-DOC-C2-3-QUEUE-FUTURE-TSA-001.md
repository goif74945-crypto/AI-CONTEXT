TASK_ID: TASK-DOC-C2-3-QUEUE-FUTURE-TSA-001
OWNER_CHAT: C-SOL-20261006-QUEUE-FUTURE-TSA
STATUS: READY_FOR_VALIDATION
PRIORITY: P1
BASE_SHA: c1f94b2c59b787a7761079362a82aefbbfca9855
WORKER_BRANCH: NEXY.AI-Test-AI-work-queue-future-tsa-4f2a91c7
CANDIDATE_SHA: 0f701f78d90eb6a136d19172079eec5f02c7e499
PR: 68
SEMANTIC_SCOPE: reject BullMQ enqueuedAt later than authoritative TSA batch time before durable dispatch claim/state/SWARM
TARGET_PATHS:
- packages/queue/payload.ts
- tests/contract/queue-payload.test.ts
- tests/integration/queue-boundary.spec.ts
MUTATION_LEASE: HELD_FOR_VALIDATION
STATIC_REVIEW: PASS / PR clean / no leased-path integration changes since base at review
RUNTIME_STATUS: NOT_EXECUTED_INFRA_BLOCKED
NEXT_ACTION: exact-SHA focused contract+integration tests; independent review; merge only after PASS and fresh race check
FORBIDDEN: NEXY.ai; host-clock authority; TTL semantic widening; dispatch/jobs mutation
