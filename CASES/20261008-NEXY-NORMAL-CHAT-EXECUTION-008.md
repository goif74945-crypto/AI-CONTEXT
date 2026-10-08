# CASE 20261008-NEXY-NORMAL-CHAT-EXECUTION-008
TYPE: CORRECTNESS / SECURITY
STATUS: OPEN_PENDING_REAL_EXECUTION
SOURCE: Verified source observations and committed worker Execution 007.
ISSUE_Q: Queue producer waits for Redis enqueue then issues ID-only durable state update. OWNER cancellation may win between operations and be overwritten by stale producer success or error path. CAS is necessary candidate but not sufficient proof; external BullMQ job and worker must be reconciled.
ISSUE_C: Linux cage can direct-spawn when bwrap probe unavailable, while seccomp policy is created as JSON without proven process-level filter. Actual production exposure remains to be established.
WHY_OPEN: Only self-contained model 5/5 was reported; no Postgres/Redis or isolation runtime proof, no product source patch.
REQUIRED: product-linked RED regression, minimal patch, real isolated integration when runner exists, backend policy match, negative tests, rollout protection.
SOURCE_HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 observed, re-query before writing.
BLOCKED_PATH: no demonstrated real runner in 007, CI pre-step failures.
NEXT: Execute COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-008.md in the same normal ChatGPT worker.
