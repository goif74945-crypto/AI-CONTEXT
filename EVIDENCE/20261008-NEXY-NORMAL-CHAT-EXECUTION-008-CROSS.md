# EVIDENCE 008 | QUEUE/CAGE and CI
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

COMMAND read live: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-008.md blob 5966a956b65a113d368caefd237315aa16f9fd5a.
PRODUCT START/NO-WRITE HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08; CONTROL PREWRITE 8e787a81e11fc00f2bd7d5ca68474f0b774085c1.
QUEUE deliverable is full exact HEAD source candidate + git apply unified diff and product-linked Vitest source using real exports dispatchDirective/cancelDirectiveDispatch/claimDirectiveDispatch/completeDirectiveDispatch. Unlike model in 007, the regression suite imports original product module. 10 tests authored; none run and no RED/GREEN claims.
QUEUE REVIEW: workers.ts claim guards PENDING|ENQUEUED via updateMany and run validates TSA TTL; redis jobId/idempotencyKey queue jobs; worker cancellation watch and commitAuthorizedPipelineRelease invoked. Unverified actual transaction and provider protection.
CAGE REVIEW: DOCX paragraphs P04137-P04149 namespace/syscall/memory isolation, P04886-P04927 tier recursion. cage.ts linux missing bwrap -> direct trusted spawn with process.env; seccompJson written to temp but not passed to bwrap; cgroup failure swallowed. No runtime exploit claimed.
CI: workflow YAML exact-head-evidence.yml blob 04fdc310d7c698ea9d695bc158f0d3b8955c62f8; e7-queue.yml blob 32c3cfa6e9daee311c9a801ec81bd08cda298ce3. Current HEAD failure runs 37741650355, 37741650349, 37741650343, 37741650376, 37741650318; 404 BlobNotFound fetching job 113193487317 logs. Github rerun_workflow_job 113193487979 returned true; require independent new run outcome read. Do not infer YAML invalid or billing cause.
CANDIDATE integrity: dispatch original full source at blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29, old function begins line 106, old length 79 lines; replacement 134 lines. CAGE anchor starts line 531. Candidate not product commit.
TSA/RELEASE: DOC-C P09945-48 stale_job_ttl_ms 900000, max_concurrent 10. No direct normative TTL-signature link proven. Core time unaffected. DOC-E approval absent.
