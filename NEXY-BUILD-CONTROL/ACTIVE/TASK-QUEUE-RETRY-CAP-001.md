TASK_ID: TASK-QUEUE-RETRY-CAP-001
OWNER_CHAT: C-SOL-20261006-0143-QUEUE-RETRY-CAP
STATUS: INTEGRATED_NOT_FULLY_VERIFIED
PRIORITY: P1
BASE_BRANCH: NEXY.AI-Test-AI
ORIGINAL_BASE_SHA: cf2da83c1a56fedbdb8812e4d2664d39ce7cc8cc
WORKER_BRANCH: NEXY.AI-Test-AI-work-queue-retry-cap-6c8f21a4
WORKER_HEAD_SHA: 753b98b212689213061b5b741c9d2ad808d3b0f4
PR: 62
INTEGRATION_SHA: 5fff467be07fd45993b2e3cfa07cc319dc4fa755
INTEGRATION_TREE: 6875952aa99ae0e0e1ad0d860b8ffa50b6b9ac53
SEMANTIC_SCOPE: DOC-C queue max-concurrent invariant on explicitly authorized retry of an existing failed BullMQ job.
TARGET_PATHS:
- packages/queue/jobs.ts
- tests/contract/queue-retry-cap.test.ts
REQUIREMENT: max_concurrent_pipeline_runs = 10 applies to new admission and explicit failed-job retry.
IMPLEMENTATION:
- shared admission-cap helper used before existing.failed.retry() and before queue.add()
- regression covers full-cap reject and below-cap retry
PREMERGE_RUNTIME_EVIDENCE:
- exact jobs.ts Git blob 95ddd27f7113ec655c9f5e95b7f4e7e77e5966c2 executed
- exact retry-policy.ts Git blob 3888169fc88784c999c31ff0f19ad673ba0e0f11 executed
- focused harness PASS: cap=10 -> RATE_LIMIT_EXCEEDED/no retry; cap=9 -> exactly one retry
- focused TypeScript compile PASS
INTEGRATION_METHOD:
- atomic Git tree+merge commit
- parent 1 latest integration head c1f94b2c59b787a7761079362a82aefbbfca9855
- parent 2 worker head 753b98b212689213061b5b741c9d2ad808d3b0f4
- update_ref used expected_sha lease and force=false
POST_INTEGRATION_EVIDENCE:
- Exact HEAD run 37360868127 at 5fff467b: FAILURE before any job step
- Six-system run 37360868111 at 5fff467b: FAILURE before any job step
- Pre-existing base c1f94b2c runs 37360804656 and 37360804659 fail the same way with zero steps
VERDICT:
- focused target behavior: PASS
- focused compile: PASS
- repository-wide exact-head: NOT_VERIFIED
BLOCKER:
- GitHub Actions runner/startup path fails before checkout/test execution; shared Railway validator is leased by T-B7E4C2A1; isolated Railway service provisioning exceeded plan resource limit.
OVERLAP:
- TASK-QUEUE-FAILED-STATE-CAS-001 owns packages/queue/dispatch.ts only; no target-path overlap.
NEXT_ACTION:
- no queue patch repair indicated by current evidence
- rerun exact-head repository gates when execution infrastructure is available
