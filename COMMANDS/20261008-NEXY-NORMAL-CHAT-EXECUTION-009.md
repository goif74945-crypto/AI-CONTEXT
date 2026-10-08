# NEXY.AI — EXECUTION 009 | SAME NORMAL CHAT | SOURCE-FENCED CROSS-STORE QUEUE CLOSURE
SYSTEM: NEXY::NORMAL-CHAT-EX009-QUEUE-CROSSSTORE-VALIDATION-V1
MODE: ทำ / EXECUTE_NOW / CROSS / SINGLE_WRITER / FAIL_CLOSED / NO_GUESS / LIVE_HEAD_FENCE / NO_FAKE_PASS / SELF_EXECUTE
WORKER: SAME EXISTING CHATGPT NORMAL CHAT THAT REPORTED EXECUTION 008. NOT CODEX; DO NOT CREATE ANOTHER CHAT.

## 0. PRIMARY OBJECTIVE
Continue the engineering task beyond mock RED/GREEN. Establish whether Queue cancellation is safe across durable PostgreSQL dispatch rows, BullMQ/Redis publication, worker claim/execution, and final output-release transactions. If safe isolated real integration can be executed, run it; only after all applicable gates pass may you consider smallest product commit. If real integration remains unavailable, add a genuinely NEW executable product-linked integration harness, negative regression and exact minimal patch candidate to AI-CONTEXT, explicitly mark NOT_RUN, and continue an independent READY source/security task. Avoid another unchanged source/model recap.

## 1. AUTHORITY / LIVE HEAD / MULTI-CHAT SAFETY
Product: goif74945-crypto/NEXY.AI-, ONLY authorized product branch NEXY.ai.
Last directly observed product HEAD when this instruction was authored: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
Control repo: goif74945-crypto/AI-CONTEXT, ONLY branch main.
Latest 008 control evidence snapshot: 85d9e9ac0f59e3bb64014ddf2a97948cc859fe21. Requery current HEADs; those numbers are not write authority.
Canonical specification: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
Required SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
DOC-C P9844 = build obligation; DOC-E P9845 = deployment approval; queue stale_job_ttl_ms 900000 (P9946) and max_concurrent_pipeline_runs 10 (P9947). Never infer an explicit final DOC-C TSA signature requirement; broader Core time law exists and is separate.
Use only real source bytes/test execution/verified Git refs. Do not force push, create/delete branch, overwrite collaborators, alter settings/secrets/protection or use production accounts/data.

## 2. VERIFY EXECUTION 008 ARTIFACTS BEFORE REUSE — CRITICAL
Our independent source review found MULTIPLE 008 candidates, not one interchangeable test suite. Do not merge claims:
A. Artifact family EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-*:
  - Base product dispatch.ts Git blob: 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
  - RED as reported: 4 pass / 5 fail; GREEN: 9 pass / 0 fail; focused four-file suite 17/17; backend typecheck pass after Prisma generate.
  - Regression test: EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cancel-race.spec.ts, Git blob 8900ea58bb5b94c5ccc5e38e2079276df3954cfc.
  - ONLY CORRECTED PATCH: EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas-FIXED.patch, Git blob b7c9444d4348fd84691cea287c9477e6c90dd734.
  - After applying FIXED patch to base, expected patched dispatch.ts blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af.
  - The ORIGINAL file ...-queue-cas.patch (blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8) is INVALID after read-back: missing final newline, git apply reports corrupt patch line 140. NEVER USE.
  - Correction proof: EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-artifact-readback-correction.md, commit 85d9e9ac..., reports reverse/forward git-apply round trip.
B. Independent 008 red/green family EVIDENCE/20261008-NEXY-008-CROSS-QUEUE-REDGREEN-FENCED-*:
  - RED 3 pass / 6 fail, GREEN 9/9; separate test blob e64653d893e5403ebf60505303c63a590a8cdcf5; patch Git blob 3296992af5276641046accc5941ed595008b63e3; patched source blob 94340b7a591e2961b03591780668352ade165394.
  - That run reported backend typecheck EXIT=2 due to Prisma generation/setup, DO NOT cite another family's typecheck PASS as its own.
C. Additional candidate: PATCHES/008/queue-dispatch-cas.patch (blob 4236bcf95a1541065053d9c77d0558f923523537). Distinct diff and no automatic GREEN proof.
D. Independently validate each candidate against frozen source, patch apply status, resulting Git blob, source-linked test import, and regression logs. Choose one only by observable semantics, minimized trusted change and rerun. Never concatenate diffs blindly. Record in a PATCH_CANDIDATE_DECISION_TABLE with path+blob+test+RED/GREEN+typecheck+missing safety proofs. If other chat has advanced product HEAD, re-evaluate the entire comparison and abandon stale patch assumptions.

## 3. AUDIT THE CANDIDATE'S RESIDUAL RISKS BEFORE PROMOTION
Patch family A uses Prisma updateMany CAS {id, status, attempts} on the success and failure paths after queue enqueue, narrows catch so DB CAS error is not rewritten FAILED, and reads durable row after a losing CAS. This prevents particular stale updates in mocks, NOT cross-store atomicity.
Required semantic challenges:
- PostgreSQL updateMany transaction atomicity at concurrency/isolation level.
- An enqueue can publish to Redis before durable CAS; BullMQ worker may claim PENDING before CAS and execute. Validate first durable worker claim, cancellation watcher and output-release commit against actual DB state.
- After CAS loses to CANCELLED, Redis job may still exist; worker MUST NOT execute provider/release, and cleanup or ignored job must not invalidate legitimate re-enqueue.
- After CAS loses to PROCESSING/COMPLETED, returning delivered:true/idempotent:true must reflect durable meaning and must not accidentally hide missing Redis job.
- Two producers/reconcilers may enqueue same BullMQ idempotency key and race; attempts must count once per valid transition; FAILED retry requires explicit safe allowlist QUEUE_UNAVAILABLE and max-attempt policy.
- Poisoned/ambiguous failures (e.g., Redis publish succeeded but client saw timeout; DB CAS unavailable) must not declare delivered false as absolute proof of no Redis job.
- Audit, pipeline run state and release flags must not be committed for cancelled directives; cancellation during already-active SWARM must be enforced at the final release boundary, not only with 250ms polling.
- "PENDING" observed after loss cannot be deemed safe/no job without checking cross-store contract.
- Core trusted time cannot be replaced with wall clock or fake TSA signatures; failure must remain fail-closed.

## 4. REAL TEST CAPABILITY DISCOVERY (DO THIS, DON'T SIMULATE)
Prior Execution 008 used a connected authorized Windows 10 Desktop Commander with Node v24.21.0, npm 11.19.0, Vitest 4.1.11 and Prisma 5.22.0 on isolated clone. No Docker, psql, redis-server was observed on that host. First determine whether the SAME authorized runner remains connected and writable; if yes use an isolated fresh checkout and rerun baseline/patch tests with immutable HEAD+blobs.
Investigate legitimate additional connected runners (authorized remote terminal/desktop, existing Linux testing environment, supported cloud dev sandbox, existing CI runner) and find whether real isolated PostgreSQL and Redis can be spun up without secrets or touching production. Creating paid cloud resources, altering account billing, downloading untrusted executables or exfiltrating private source needs valid authorization and security controls. If unavailable, preserve NOT_RUN and create an executable integration harness to run later. Never describe a mock as real PostgreSQL+Redis.
Inspect repository package scripts, Prisma migrations/schema, BullMQ config, Redis AOF requirements, worker startup and test fixtures. Capture exact command, exit, full sanitized stdout/stderr, tool+node versions, test identifiers and SHA. Ensure no live production DB/Redis or tenant data.

## 5. REQUIRED INTEGRATION TEST MATRIX
Add source-linked isolated tests (use real PostgreSQL/Redis where possible) with deterministic barriers, recorded expected vs actual state:
T01: cancel before producer read (no publish/no provider execution).
T02: cancel during pending enqueue success.
T03: cancel during enqueue throw.
T04: cancel after Redis publish before producer durable CAS, including worker claim early.
T05: worker claims PENDING before producer ACK then OWNER cancels during execution.
T06: duplicate producers/reconcilers and retry of same BullMQ jobId under idempotency.
T07: FAILED retry safe-error allowlist and maxAttempts exhaustion.
T08: DB CAS throws after Redis publish; distinguish uncertain publish side effect and recover.
T09: Redis timeout after actual publication (ambiguous network acknowledgement).
T10: crash/restart in enqueue/DB-update gap; durable reconciliation and no unauthorized execution.
T11: cancel after SWARM response but before JUDGE/LAW release; require transactional output gate.
T12: TTL expires using authorized TSA-injected time; preserve stale TTL 900000, never local clock.
T13: DB or Redis service interruption/restore, no invalid terminal state resurrection.
T14: idempotency/audit/failed-session tenant isolation where applicable.
For each test capture database row (status, attempts, lastError, enqueuedTick), BullMQ state/job id, worker claim result, provider invocation count, LAW release/output state and audit receipts. An isolated test environment is required for user data safety. If a test requires real network/service interleaving and mocks are used, label as MOCK_TEST, not E2E/INTEGRATION_VERIFIED.

## 6. PATCH / COMMIT DECISION (DO NOT BLOCK ALL READY WORK)
Gate G1 provenance: current NEXY.ai HEAD and exact source blob match base or fresh source analysis completed.
Gate G2 validity: chosen patch applies cleanly; source-linked tests turn expected RED into GREEN; no regression weakened; typecheck/build + test commands executed and captured.
Gate G3 cross-store: real PG/Redis worker interleaving validates cancellation finality, ambiguous Redis publication, and durable output release. If G3 is NOT_RUN, do NOT label queue closure VERIFIED or release-ready. Whether to commit code must also respect existing user-requested cautious product-write gate; prefer keeping untested high-risk patch in AI-CONTEXT pending G3 rather than committing.
Gate G4 security: no clock/TSA forgery, secret exposure, sandbox bypass, privilege or tenant issue.
Gate G5 single-writer: requery HEAD, confirm unchanged source blobs, atomic fast-forward commit only on NEXY.ai when authorized and safe, read-back exact changed files and tests, verify regression on final HEAD. No unsafe force/overwrite or branch topology mutation.
If runner missing, deliver repo-integrated PG/Redis test harness and untested patch candidate to AI-CONTEXT instead of recycling 9/9 mocks. Continue another READY requirement audit or explicitly bounded security patch test. No false product mutation claim.

## 7. CAGE & CI WORKSTREAM
CAGE: source cage.ts blob 5afd464ed39470381ef1df643a630e1f431817dc at old HEAD. When bwrapAvailable false, direct spawn bypasses namespace and seccomp is written as JSON without verified process enforcement. Trace production/restriction gates; production protected code must fail closed if required isolation unavailable. Run Linux bwrap/unshare/seccomp/cgroup negative tests using real isolated runner if available; do not silently weaken or downgrade to dev-naive. If not, prepare exact versioned negative tests + bounded patch as NOT_RUN.
CI: five push workflow runs on observed 44bcb851 head all failure: 37741650349, 37741650343, 37741650376, 37741650355, 37741650318. Previously inspected jobs had runner_name="" and steps=[]. This proves pre-step failures for inspected jobs, but does not identify cause. Inspect check annotations, job logs, runner labels and repo workflows; do not blame billing, YAML or tests without evidence; do not edit settings, protection or alter required gate. Treat inaccessible logs as root cause UNKNOWN.

## 8. MATRIX / EVIDENCE / FINAL GATE
Read 98-row canonical matrix using exact authority and source locator, distinguish newly verified/source-only/mock-tested/real integration-tested/not-reassessed, separate SUBSTANTIVE_AUDIT_COVERAGE from COMPLETION. Execution 008 reported 16 of 98 examined to varied depth, 82 NOT_REASSESSED, and completion NOT_COMPUTABLE. Do not combine competing 008 matrix snapshots as independent unique rows; deduplicate by requirement ID and HEAD.
Keep temporary task log with input/output/error/status and hashes. Before end freeze HEAD, read memory first-to-last, dedupe IDs, detect conflicts, verify all cited source heads and negative claims, read back files.
Write sanitized TASKS/LEDGER/CASES/FAILURES/EVIDENCE and, if relevant, TESTS/PATCHES for Execution 009 into AI-CONTEXT/main; read-back all persisted files and record resulting head. If impossible: AI_CONTEXT_WRITE_FAILED and complete import package, no fictitious saved claim.
Release remains NOT_AUTHORIZED without DOC-E human approvals, exact-head CI, rollback rehearsal and monitoring proof. NO background promises; work only through actual tool calls in this turn.

## 9. MANDATORY MEASURABLE OUTPUT
This turn must meaningfully advance beyond Execution 008, not simply rehash source findings:
- Best: execute REAL isolated Postgres+Redis tests and resolve all critical queue races, then, if every gate passes, commit smallest tested product change.
- If impossible: produce an actionable, product-importable PG+Redis E2E harness with source/test paths, preconditions and concrete assertions; run all feasible repo-level checks; identify exact missing capability; then audit a separate READY security/architecture area.
- Do NOT count a further identical 9/9 mock replay as completion of E2E proof.

FINAL REPORT:
MODE / STATUS / LIVE_HEADS_START_END / SOURCE_SHA / CANDIDATE_DECISION_TABLE / TEST_EXECUTION_COMMANDS_AND_EXITS / RED_GREEN_PROVENANCE / PG_REDIS_E2E_STATUS / WORKER_RELEASE_FENCE / CAGE_STATUS / CI_FAILURE_ROOT_CAUSE / PRODUCT_CHANGES / CONTROL_COMMIT_READBACK / 98_ROW_MATRIX_COVERAGE / COMPLETION_DENOMINATOR / DOC_E_RELEASE / BLOCKERS / NEXT_READY_ACTION / VERDICT (PARTIAL unless all gates truly pass).
BEGIN NOW IN SAME NORMAL CHAT.