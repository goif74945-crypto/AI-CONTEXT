# NEXY.AI — NORMAL CHAT EXECUTION 011 | CLOSE THE REAL RUNNER GAP, TEST LOCK ORDER, AND IMPLEMENT READY WORK
SYSTEM: NEXY::EX011-EVIDENCE-LOCKED-RUNNER-OR-ALTERNATE-ENGINEERING-V1
MODE: ทำ / EXECUTE_NOW / CROSS / SINGLE_WRITER / SELF_EXECUTE / FAIL_CLOSED / CURRENT_HEAD_AWARE / NO_FAKE_PASS
EXECUTOR: SAME ORDINARY CHATGPT CHAT THAT PRODUCED EXECUTION 010, NOT CODEX, NO NEW CHAT.
MISSION: Do actual verifiable engineering; resolve an isolated PostgreSQL/Redis runtime route if authorized and available, test source-linked producer/worker/OWNER cancellation against it, or complete an independent executable READY engineering task while G3 remains frozen. Do not make a sixth source-only/compile-only queue "progress" claim in place of G3.

## 0. EVIDENCE ENTRY CHECK
Product repository: goif74945-crypto/NEXY.AI- , ONLY branch NEXY.ai.
Directly observed HEAD on command authoring: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
Coordination: goif74945-crypto/AI-CONTEXT, ONLY main.
Directly observed EX010 control HEAD: d71d52f4d384f82c5e27a4edf7593f958c120c1a.
These are NOT unconditional write bases: REQUERY current branch heads, blob SHA, diff and access before each mutation and at final gate. Concurrent chats exist; no force push, branch creation/deletion, reset, settings/protection/secret changes or hidden conflict resolution.
Authoritative DOCX: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx, required SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7. DOC-C P9844 controls build, DOC-E P9845 release approval. Do not claim to rehash DOCX in THIS chat unless bytes directly available. Earlier hash report is evidence provenance, not automatic current file access.

READ THESE EXACT CONTROL SOURCES before work:
- TESTS/010/ex010-real-producer-crossstore.mts (Git blob ffff2888b8fc921415b0f1e6c77d2df9f5aa3036)
- TESTS/010/README.md (blob 5c81ced5b0440993f62516dcfc5f5dbd84047ddc)
- TESTS/010/docker-compose.yml (blob 730d81f746b9e249ad91e602f792ff4c3c3c0d35)
- TESTS/010/ex010-owner-cancel-transaction-scope.spec.ts (blob fdafbf4f238de5c7f8bcd249fc750cc3d6779808)
- EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-CROSS-cancellation-source-correction.md (blob 74b0200b841edfc56204b52b7bb0a93b6c3f8b90)
- EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-CROSS.md
- EVIDENCE/20261008-NEXY-NORMAL-CHAT-EXECUTION-010-CROSS-98-matrix.tsv
- Related 008 candidates and 009 decision table.
The EX010 matrix is 98 distinct requirement IDs, 80 explicitly NOT_REASSESSED_010, 18 of mixed scope, not 18 passed or 18% complete.

## 1. ACCEPT OWNER CANCEL CORRECTION AND INVESTIGATE ONLY NARROW REMAINING RACES
At product HEAD 44bcb851: packages/queue/run-state.ts Git blob e162efc8b2a45014bcefbd60dc67a95d8a1e1003, packages/queue/dispatch.ts Git blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
VERIFIED SOURCE: canonical cancelPipelineRun() -> recordPipelineRunFailure({cancelDispatch:true}) -> prisma.$transaction -> lockPipelineRun(tx,pipelineRunId) -> pipelineRun FREEZE/accepted=false/releaseable=false + directiveDispatch CANCELLED in same transaction. commitAuthorizedPipelineRelease() obtains same advisory lock and calls assertDispatchNotCancelled before STABLE. emitAuthorizedPipelineOutput() also locks and checks STABLE/accepted/releaseable before emission.
DO NOT REPEAT the now-corrected blanket accusation "canonical OWNER cancellation lacks advisory lock" or call it a confirmed exploit. The 5/5 EX010 Vitest tests were SOURCE-CONTRACT string/order checks, not PostgreSQL concurrency tests.
NARROW UNKNOWN: standalone cancelDirectiveDispatch() has guarded updateMany without that advisory lock; canonical cancel invokes it as cleanup, but prove whether ANY reachable alternate writer/callsite changes dispatch outside the canonical transaction; determine whether a contradictory STABLE + CANCELLED durable state could legally arise. Source alone does not certify reachability or exploit.
Required real concurrency test when service is possible: use TWO independent PostgreSQL transactions/connections, controlled barriers and documented lock acquisition order; race OWNER cancel vs LAW STABLE/release vs standalone cancellation and check durable invariant. Account for whichever transaction linearizes first. Assert persisted runState, dispatch status, accepted/releaseable, emitted marker and audit receipts; don't treat an authorized output committed-before-owner-cancel as the same as unauthorized output-after-cancel. Do not patch lock behavior without a failing test/authority proof.

## 2. STOP THE RUNNER-DEADLOCK WITH FINITE REAL CAPABILITY DISCOVERY
Previous worker reports: authorized Windows laptop Node/npm, no Docker/Podman/Redis/Postgres native, WSL failed, isolated Linux apt update timed out, Termalin no hosts, connected Railway NEXY Validation R2 stores only in environment named production and were correctly NOT used. CI E7 run 37741650376 attempt 2 on product HEAD failed before job steps, with six jobs runner empty and steps=[]; no root cause evidence.
This is historical. In this execution, use REAL current connected tool capability to check AT MOST a small set of concretely distinct, authorized execution paths:
1. existing user-authorized machine runner/service: read-only discover active Docker/Podman/PSQL/Redis or existing isolated container runtime; check actual process, ports and permissions, no assumptions;
2. existing authorized development workspace/terminal with ephemeral disposable containers; discover permission with safe reads, not an unauthorized cloud app install;
3. actual available CI runner/logs if job can execute (no blind repeated reruns, no disabling gates).
Do NOT consume time rerunning "no Docker" probes multiple times without a change. Treat inaccessible authorized tool as ACTION_BLOCKED and continue alternate work.
Do not touch production Railway DB/Redis, create/clone paid resources, change billing or use owner secrets without explicit approval. Do not download/execute untrusted binaries from arbitrary websites. Do not repurpose any existing user's database as disposable. Do not weaken GitHub Actions and don't guess why steps are absent.
If feasible, create a uniquely isolated loopback-only PG/Redis instance, use named ephemeral test DB with dedicated credentials and namespace, verify health and Redis AOF, run migrations on ONLY that DB, and guarantee cleanup of your own test resources. Record exact commands, version numbers, exit statuses, redacted outputs, and read-back.

## 3. IF REAL SERVICES ARE AVAILABLE, RUN EX010 HARNESS AND PROVE ACTUAL PRODUCER PATH
Use a fresh isolated checkout of NEXY.ai and single candidate patch only. Source before 008 candidate A: dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29. Candidate A FIXED patch blob b7c9444d4348fd84691cea287c9477e6c90dd734, expected patched source 36e56aef98a5b8b52f644a0178eb3638d2c4b9af; original uncorrected patch blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8 is invalid. Candidate B blob 3296992af5276641046accc5941ed595008b63e3 and C blob 4236bcf95a1541065053d9c77d0558f923523537 are distinct. Never borrow tests/pass results across patch families; revalidate source/patch/test SHA before applying.
The EX010 harness calls real dispatchDirective()->enqueueDirective()->BullMQ Queue.add + Prisma, with a TEST-ONLY intercept AFTER Redis publication, test-only UNSIGNED injected TSA batch, and a PROBE WORKER rather than packages/queue/workers.ts. First audit harness assumptions for deadlocks, resource cleanup and schema mismatch; don't falsely call it prod E2E.
Run actual isolated service test and capture per-case:
P1 cancel after real publish before producer CAS -> CANCELLED immutable, zero unauthorized release;
P2 ACK failure after real Redis publish + cancel -> no false absence claim/no FAILED overwrite;
P3 early worker claim PENDING -> no status rewind/double attempts;
P4 concurrent producer/reconciler job IDs and at-most-one valid attempt;
P5 probe worker refuses cancelled jobs before invoking test provider;
LAW1 canonical OWNER cancel vs transaction commit ordering using actual advisory lock;
LAW2 standalone dispatch cancel vs final output emission contradiction probe if source risk survives;
RUNNER0 service ready/migrations/AOF check.
State the tested depth separately: source contract, mock producer, REAL PG+Redis producer with probe worker, and FULL production worker. TEST_ONLY_TIME_INJECTION is NOT verified TSA signing. Source-based release lock evidence is NOT transaction race PASS. If T00, P1-P5 pass but no real production worker, mark real producer+probe verified only, not full E2E.
If a case fails, diagnose first with exact exit and committed database/queue snapshots; smallest patch+regression only after proven root cause. No cherry-picked successes.

## 4. IF REAL SERVICES STILL UNAVAILABLE, PIVOT TO A DIFFERENT READY WORKSTREAM, NOT ANOTHER E2E HARNESs
Output runner capability matrix as hard evidence with named attempted tools and precise BLOCKED reasons. Do NOT keep adding service harness versions that cannot execute. No more identical mock/source tests counted as forward G3 completion.
Next choose ONE independent scope from authoritative DOC-C with actual accessible proof and test runner:
- inspect exact requirement and source for API/Auth/session, queue-independent determinism, contracts/schema, configuration, RBAC or coverage/CI static checker;
- identify a concrete failing source/contract behavior; implement smallest isolated fix with RED/GREEN product-linked tests and typecheck on an authorized local runner;
- on success, only if product-write scope/current HEAD/permission/test gates allow, commit atomic change to NEXY.ai with source+tests and read-back; if not, store production-importable patch and executed tests in AI-CONTEXT, NOT_COMMITTED.
Do not fabricate an additional requirement or change architecture merely to create progress. Prefer the highest-risk ready finding with independent executable regression; avoid sandbox fixes that require unavailable Linux proof.
Alternatively investigate a specific accessible CI pre-step failure from current GitHub run/job diagnostic data to its first verifiable cause; unless supported by logs/annotations, leave ROOT_CAUSE_UNKNOWN and move on.
If NO independent ready work can be executed, document exact blocker and stop accurately with PARTIAL; don't produce a hollow task completion.

## 5. SECURITY AND RELEASE
Preserve fail-closed TSA authority; no Date.now or synthetic quorum in Core. DOC-C queue TTL 900000ms, concurrency 10; no falsely asserted TSA-signature queue-expiry clause. Any fixture injection must be isolated to test process and labelled UNSIGNED.
Cage source-contract candidate blocked by absent Linux namespaces/seccomp/cgroup verification; do not claim OS isolation because strings/test counts pass. No untrusted process may be deployed without required sandbox protections.
No production deployments, rollback claims, DOC-E approvals or human signoff fabrication. Do not lower assertions, skip CI, change allowlists, force push, or mutate product security settings.

## 6. COVERAGE, TEMP LEDGER, AI-CONTEXT CLOSE
Create temporary WORK_LOG in tool-accessible workspace if possible, recording input source commit/blob, action, output, test exits, mutation, errors, decisions; re-read it first-to-last at close. If no workspace, use explicit session ledger and mark SESSION_ONLY.
Audit new requirement rows only with original DOC-C paragraph, exact current HEAD/source blob and live test depth. EX010 had 98 distinct IDs and 80 NOT_REASSESSED. Do not count NOT_REASSESSED as failed or passed. SUBSTANTIVE_AUDIT_COVERAGE and ASSESSED_COMPLETION_PERCENT use separately defined denominators; no unjustified "18% complete".
Persist sanitized artifacts using NEW 011 task IDs to AI-CONTEXT/main: TASKS, LEDGER, CASES, FAILURES, EVIDENCE, and executable TESTS/PATCHES when created. Read back all files and GitHub HEAD after write. If write fails, AI_CONTEXT_WRITE_FAILED + AI_CONTEXT_IMPORT_PACKAGE. Never claim NEXY.ai changed if it did not.

## 7. FINAL GATE / OUTPUT
A substantive 011 result must be EITHER:
A) actual isolated service test with real Postgres+Redis and producer / cancellation / release evidence, OR
B) distinct, testable DOC-C repair with actual source-linked executed regression (and safe commit where permitted), OR
C) concrete independently verified diagnostic cause for prior CI pre-step failure with proof.
A non-executable harness compile alone is not a completed G3 test. If A/B/C blocked, report verified blockers and realistic alternate paths rather than claiming pass.
Report:
MODE:
STATUS:
PRODUCT_HEAD_START/END:
CONTROL_HEAD_START/END:
AUTHORITATIVE_SPEC_ACCESS:
RUNNER_DISCOVERY_ATTEMPTS:
POSTGRES_REDIS_SERVICE_RECEIPTS:
PRODUCER_AND_PROBE_RESULTS:
OWNER_CANCEL_TRANSACTION_RACE:
STANDALONE_CANCEL_REACHABILITY:
CI_ROOT_CAUSE_STATUS:
INDEPENDENT_READY_FIX:
PRODUCT_CHANGED_FILES/COMMIT:
AI_CONTEXT_CHANGED_FILES/COMMIT/READBACK:
98_ROW_COVERAGE_TABLE:
AUDIT_COVERAGE:
ASSESSED_COMPLETION_PERCENT:
TESTS_ACTUALLY_RUN / TESTS_NOT_RUN:
RISKS:
BLOCKERS:
DOC_E_RELEASE:
VERDICT:
Use PARTIAL, FROZEN_PATH or VERIFIED_WITH_LIMITS accurately; not 100% or PROD_READY without direct evidence.
EXECUTE NOW, SAME NORMAL CHAT, NOT CODEX.