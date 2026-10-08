# TASKS Execution 008
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

- [x] Read canonical 008 command, 007 source, LIVE product/control HEADs
- [x] Recompute canonical DOCX SHA256 from mounted bytes
- [x] Check runner readiness: desktop timeout, Termalin none, GitHub workflow E7 rerun accepted
- [x] Generate SOURCE-LOCKED full product queue candidate + unified diff; not applied to product
- [x] Generate 10 product-import Vitest regression cases with deterministic barriers, mock boundary; NOT_RUN
- [x] Generate separate minimal cage fail-closed patch candidate, NOT_RUN
- [x] Inspect current CI YAML, pre-step failures and failed log fetch
- [x] Inventory 98 requirements, 13 source-triage rows, rest explicitly NOT_REASSESSED
- [ ] Execute original RED and candidate GREEN on actual product dependency graph
- [ ] Execute PostgreSQL+Redis isolated concurrency/worker/release tests
- [ ] Enforce full cgroup/seccomp/namespace isolation and negative test
- [ ] DOC-E signed release gate, rollback drill, monitoring; RELEASE_BLOCKED
NEXT_READY: Recheck E7 run state; obtain authorized isolated runner; stage candidate in clone and run RED/GREEN and DB/Redis proof, then decide on minimal product commit using fresh HEAD + blob fencing.

## POST-COMMIT CI ATTEMPT-2 & PATCH REVIEW (append only)
- GitHub rerun_workflow_job returned success=true for old job 113193487979, E7 run 37741650376.
- GET run 37741650376 now reports attempt=2, status=completed, conclusion=**failure**, tested product SHA 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
- Attempt-2 NEW job 113320413296 (Real Redis/BullMQ E7 gate) ended **failure**, steps=[].
- Attempt-2 job log fetch returned 404 Azure BlobNotFound, root cause STILL UNKNOWN; no Postgres/Redis test PASS.
- Reviewer identified original zero-context .patch hunks and fixed with three context lines; queue patch and full candidate source now generated from same source-line replacement. NOT_RUN: git apply --check and Vitest, pending actual runner.
