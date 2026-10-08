# NEXY — NORMAL CHAT CONTINUATION EXECUTION 007
SYSTEM: NEXY::SOURCE-PROVEN-QUEUE-CANCELLATION-AND-CAGE-CLOSURE-V1
TARGET: SAME ACTIVE CHATGPT NORMAL CHAT ("แชททำ"), NOT CODEX; DO NOT SPAWN OTHER CHATS

MODE: ทำ / EXECUTE_NOW / CROSS / ENGINEERING / EVIDENCE_DRIVEN / FAIL_CLOSED / CURRENT_HEAD_FENCED / SINGLE_WRITER / CONTINUE_READY_WORK
STATUS_ON_ENTRY: PARTIAL / NOT_RELEASE_AUTHORIZED

## 0. TASK AND SOURCE FENCE
Your prior handoff 006 was an honest source-only audit, not an implementation repair. Continue executing in this same normal ChatGPT conversation through genuinely connected tools. Do not stop at ACK, planning, or another source-only recap if a safe READY path exists.

Product: goif74945-crypto/NEXY.AI-
Allowed product branch only: NEXY.ai
Last independently observed product HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control: goif74945-crypto/AI-CONTEXT, branch main only
Last independently observed control HEAD before this command: 07e3a8f690d84f6da97850387450b4b307727453
These HEADs are OBSERVATIONS, not unconditional write bases. Re-query both before reads/writes and after every commit. Other ChatGPT chats may be working concurrently. Do not force-push, reset, change branch topology, settings, secrets, permissions, or protection.

Authoritative DOCX name: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
Required SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
DOC-C controls BUILD requirements (P9844); DOC-E controls deployment approval (P9845).
Relevant previous evidence:
- AI-CONTEXT/EVIDENCE/20261008-NEXY-HANDOFF-006-CROSS.md
- AI-CONTEXT/CASES/20261008-NEXY-HANDOFF-006-CROSS.md
- AI-CONTEXT/FAILURES/20261008-NEXY-HANDOFF-006-CROSS.md
- AI-CONTEXT/EVIDENCE/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-CLAUSES-005.md
- AI-CONTEXT/EVIDENCE/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.tsv

## 1. NO FALSE TOOL CONCLUSIONS
A 403 REPOSITORY_READ_ONLY from Repo Code Bridge's ci_dispatch is only proof that THAT action failed, not proof GitHub connector writes, tests, all runners, or entire task are impossible. Inspect real authorized capabilities available in your own chat (GitHub operations, remote command runner, connected development environment, CI logs/re-run, safe ephemeral service runner). Do not pretend to have one. Never give secrets to a new plugin. If no executable runner is reachable, continue independent source/test-design work but distinguish NOT_RUN explicitly.
GitHub combined statuses=[] and a PR-filtered workflow-runs query do not prove no workflows exist. Check actual branch/head GitHub Actions run listings and job steps using authorized read operations; never invent a CI PASS.

## 2. FIRST PRIORITY: QUEUE-CANCEL-RACE-006
This is a source-reachable concurrency flaw, not a measured production incident.

At observed product HEAD 44bcb851, packages/queue/dispatch.ts source lines 110-182:
- fetches dispatch row before enqueue,
- awaits enqueueDirective,
- then performs prisma.directiveDispatch.update({where:{id:row.id}}) to ENQUEUED,
- catch similarly writes FAILED by id alone.
cancelDirectiveDispatch lines 301-319 can concurrently mark CANCELLED.
Worker claim uses guarded updateMany, and worker watches cancellation, but enqueue is an external Redis side effect before the producer DB commit. Treat DB + Redis + worker semantics as a SINGLE correctness problem.

MANDATORY EXECUTION PLAN:
A. Read current HEAD versions of dispatch.ts, jobs.ts, workers.ts, retry-policy.ts, run-state.ts, relevant Prisma schema/migrations and existing tests before choosing a patch.
B. Trace exact permissible dispatch states and transition table; include PENDING, ENQUEUED, PROCESSING, COMPLETED, FAILED, CANCELLED, explicit safe FAILED retry, duplicate reconciliation and crashes.
C. Reproduce the real interleaving with controlled barriers/deferred promises. Model-only test is NOT a PostgreSQL+Redis proof. Prefer executable repo tests; real isolated Postgres/Redis needed for final race-closure claim. Do not touch production services/data.
D. Apply the smallest source-justified fix that prevents a stale producer from changing a CANCELLED/COMPLETED/PROCESSING row to ENQUEUED/FAILED. Compare-and-set (conditional updateMany with status/version/attempts and affected-row count) is one candidate, NOT a substitute for examining Redis side effects and worker races. If CAS loses, do not report delivered=true for a CANCELLED row, do not increment attempts or alter terminal state. Re-read current durable state and return a truthful result.
E. Explicitly analyze the critical gap: a BullMQ job may have been published before the DB CAS failure and may already be acquired by a worker. Prove worker claim and cancellation guard prevent forbidden provider execution/release. If a two-phase outbox/handshake or state adjustment is necessary, demonstrate schema/spec compatibility and recovery after failure; do not introduce a new status without verifying contracts. Confirm no duplicate processing or lost jobs if worker sees PENDING before producer update.
F. Preserve idempotency keys, stale TTL 900000 ms, safe FAILED retry allowlist, maxAttempts, monotonic tick, cancel semantics, audit trail and atomic state transitions. Do not replace authoritative Core time with Date.now/new Date or fabricate TSA.
G. Test (applicable variants): cancel during successful enqueue; cancel during enqueue throw; cancel before dequeue; cancel while processing; retry FAIL + cancel; concurrent reconcilers; duplicate BullMQ deliveries; enqueue succeeded / DB CAS failed; crash after DB commit / before Redis; aborted worker / release fence; DB unavailable. Assert exact final durable DB row, BullMQ job state, zero unauthorized provider release, attempts, lastError, and audit receipts.
H. Tests first (RED), minimal source repair (GREEN), regression tests, type checks, static/lint, queue-contract, current-head integration. If runner truly unavailable, write a concrete smallest patch + tests with exact blob provenance to AI-CONTEXT for later verification; DO NOT commit a critical untested product fix or claim repair completion.

## 3. SECOND PRIORITY: CAGE-ISOLATION-006 (SECURITY)
At observed HEAD packages/phase-f/lo3/cage.ts Linux code:
- bwrapAvailable() can return false.
- runLinuxCgroupSeccomp() then spawns trusted executable directly without bwrap.
- seccompJson is written but no syscall enforcement was observed in this path.
- The function still returns backend "linux-cgroup-seccomp".
- cgroup write failures are swallowed; Windows dev-naive fallback also exists.
Risk: isolation may be weaker than the backend label suggests, but actual effective constraints and applicable design authority need confirmation.

MANDATORY:
A. Inspect all call sites and mode/feature gates including NEXY_CAGE_ENABLED, production vs explicit development/testing. Determine whether untrusted data can execute in this fallback in deployed paths.
B. Read DOCX sandbox scope P4137-P4149 and P4886-P4927 and DOC-C authority; do not invent a deployment policy.
C. If protected execution requires OS isolation and it is absent, fail closed with explicit reason (do not execute untrusted command), record actual backend capability/limitations truthfully, and keep any development-only fallback strictly separated and intentionally authorized, not silently triggered.
D. Never mark seccomp applied because JSON was written. Verify actual process enforcement; if not implemented, keep it UNVERIFIED or implement with a reviewed authentic mechanism if required and feasible. Do not claim OS isolation merely because runtime paths were mounted read-only.
E. Negative tests: bwrap unavailable; bwrap installed but namespace denied; cgroup unavailable/permission denied; seccomp unavailable; path traversal/symlink; /opt parent executable dynamic libs; host secret reads; forbidden network/mount/system calls; unsupported OS; privilege escalation; config injection. Run on a real isolated test runner when available. Do not delete/skip tests or weaken security to get green.
F. Separate observed source risk from verified exploit. A targeted tested fix may be committed in an atomic separate commit, with source/HEAD re-checks.

## 4. TSA PATH: SEPARATE FENCE, NO GUESS
DOC-C P9945-P9948 sets stale_job_ttl_ms=900000, max_concurrent_pipeline_runs=10 but does NOT explicitly mandate direct TSA-signature verification for queue expiry.
Broader time law P5151-P5158 forbids Core system-clock usage; P4003-P4009 contains 3 TSA / >=2 valid signatures. Queue code uses currentTsaBatchTimeMs(), and worker validates TTL against that boundary.
Before changing TSA coupling, prove the applicable authority relation and trusted injection call graph. NEVER insert Date.now, synthetic time, fake signatures, or weakened quorum. If missing normative bridge, freeze only this path; continue QUEUE cancellation correction and security review where independent. Distinguish "TSA dependency unavailable" vs "the queue must not use TSA", which has not been proven.

## 5. WRITE / TEST / RELEASE INTEGRITY
- Check live NEXY.ai HEAD and exact file blob SHA immediately before every product mutation; if drift, inspect diff and rebase your planned patch conceptually, do not overwrite.
- One source-proven root cause per smallest atomic commit where practical; new commit fast-forward only; inspect returned commit/tree, read back all changed files, record start/end HEAD and code/test diff.
- NEVER fake a test result, cherry-pick a stale PASS, weaken an assertion, delete a test, lower a coverage threshold, bypass security or disable a required CI gate.
- Passing unit/contract tests is not enough to certify Redis+Postgres race closure or sandbox isolation if the necessary integration tests have not run.
- No release/deployment approval without DOC-E signoffs, application rollback proof, monitoring, incidents and executable current-head CI. Human signoffs cannot be generated by AI.

## 6. PARALLEL READY WORK / MATRIX
If first path is blocked by inability to run critical tests, continue safe source-level coverage, contract/architecture audit and safe test/patch development, rather than stop entire request. Reassess 98 requirement IDs against the CURRENT product HEAD one by one. The prior "14 VERIFIED, 9 PARTIAL, 4 MISMATCH, 62 NOT_VERIFIED, 4 SPEC_SOURCE_ACCESS_BLOCKED, 5 INFRA_BLOCKED" matrix and 39/98 reviewed rate belong to older HEAD 8b406a63. Do not transplant percentages or statuses to new HEAD.
Calculate substantive audit coverage = source+behavior audited rows / 98. Calculate completion from evaluated normative rows only, with numerator/denominator explicitly defined. NOT_VERIFIED is neither pass nor fail. Provide one per-subsystem table, along with separate proof depth.

## 7. CLOSEOUT + AI-CONTEXT (REQUIRED)
On finishing this live execution turn, write evidence-bound sanitized artifacts to AI-CONTEXT/main:
- TASKS/<TASK_ID>.md
- LEDGER/<TASK_ID>.md
- CASES/<TASK_ID>.md for security/concurrency incident
- FAILURES/<TASK_ID>.md for blocked actions / failed tests
- EVIDENCE/<TASK_ID>.<md|tsv> including status, source blobs, test commands, raw failure outputs (redacted), exact HEADs, source-to-claim linkage, regression results, rollback.

Read back every file. If control write blocked, output full AI_CONTEXT_IMPORT_PACKAGE and mark AI_CONTEXT_WRITE_FAILED.
Maintain temporary execution memory/ledger during work; final consistency audit: freeze HEAD; re-read memory start-to-end; deduplicate IDs; detect conflicting evidence; verify provenance/head for all claims; re-check stale and negative claims; do not count unverified as 0/100; separate completion from audit coverage; list every subsystem. If tools cannot persist temporary memory, make an explicit session ledger and do not pretend filesystem persistence.

## 8. MANDATORY REAL PROGRESS
Requery HEAD and reread handoff 006. Then perform at least ONE actual READY engineering action in this chat beyond summarizing findings (e.g. executable targeted RED regression, source-bounded minimal patch plus verifiable test code saved to evidence, or completed source-to-source contract audit with line/hashes and a concrete patch plan). Pursue a real product patch only if permissions+concurrency+testing gate support it. Do not wait for a new user confirmation where existing permission suffices. If no product runner available, record an unambiguous blocker and continue independent READY work without falsely claiming product repair.

## FINAL OUTPUT
MODE:
STATUS:
PRODUCT_HEAD_START:
PRODUCT_HEAD_END:
CONTROL_HEAD_START:
CONTROL_HEAD_END:
SPEC_SHA256_STATUS:
SOURCE_PROOF:
QUEUE_RACE_BEFORE_AFTER:
WORKER_REDIS_FENCE:
CAGE_ISOLATION_VERDICT:
TSA_AUTHORITY_VERDICT:
RUNNER_CAPABILITY:
CHANGED_FILES:
COMMITS:
TESTS_EXECUTED:
TEST_RESULTS:
CI_STATUS:
MATRIX_PER_SYSTEM:
AUDIT_COVERAGE:
ASSESSED_COMPLETION_PERCENT:
DOC_E_RELEASE_STATUS:
EVIDENCE_WRITTEN_AND_READ_BACK:
REMAINING_BLOCKERS:
NEXT_READY_ACTION:
VERDICT:
TAGS: [F] [V] [A] [U] [M] [X] [N]

BEGIN NOW, SAME NORMAL CHAT. NOT CODEX. DO REAL WORK AND PROVE IT.