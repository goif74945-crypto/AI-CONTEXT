# FAILURES / BLOCKERS 008
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

1. Desktop Commander listed device DESKTOP-FOB7IK8 ONLINE, but read-only get_config and PowerShell probe TIMED OUT; ping also timed out; no command executed/proved.
2. Termalin hosts_list=[]; no remote server available.
3. Local isolated container Node v22.16.0 + TypeScript present, but no vitest/@prisma/client/bullmq/Redis/Postgres binaries or GitHub DNS; cannot execute linked repo test or real integration.
4. GitHub Actions five failed workflows from exact source HEAD with steps=[]; E7 single-job rerun API returned success=true during this execution, but run outcome still NEEDS NEW OBSERVATION; acceptance is NOT PASS.
5. Fetch_workflow_job_logs for exact-head failed with 404 Azure BlobNotFound; root cause not established. Workflow .github/workflows/e7-queue.yml and exact-head-evidence.yml define ubuntu-latest steps and Postgres/Redis services, so absent steps is pre-step, not proof of test failures.
6. Cage seccomp policy JSON has no observed attachment; cgroup setup failures explicitly swallowed. Need real system call/isolation tests and DOC-C scope mapping.
7. Authenticated production signed TSA injection not end-to-end verified. Do not substitute system clock or fake TSA. DOC-C queue TTL 900000 and cap 10 retained.
8. Completion 98 rows not established; matrix inventory retains explicit NOT_REASSESSED.

## POST-COMMIT CI ATTEMPT-2 & PATCH REVIEW (append only)
- GitHub rerun_workflow_job returned success=true for old job 113193487979, E7 run 37741650376.
- GET run 37741650376 now reports attempt=2, status=completed, conclusion=**failure**, tested product SHA 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
- Attempt-2 NEW job 113320413296 (Real Redis/BullMQ E7 gate) ended **failure**, steps=[].
- Attempt-2 job log fetch returned 404 Azure BlobNotFound, root cause STILL UNKNOWN; no Postgres/Redis test PASS.
- Reviewer identified original zero-context .patch hunks and fixed with three context lines; queue patch and full candidate source now generated from same source-line replacement. NOT_RUN: git apply --check and Vitest, pending actual runner.
