# NEXY.AI — NORMAL CHAT EXECUTION 010 | REAL SERVICE PROOF & PRODUCTION-PATH TEST COVERAGE
SYSTEM: NEXY::EX010-INTEGRATION-RUNNER-AND-REAL-PRODUCER-WORKER-GATE-V1
MODE: ทำ / EXECUTE_NOW / CROSS / SINGLE_WRITER / EVIDENCE_DRIVEN / FAIL_CLOSED / NO_GUESS / SELF_EXECUTE
WORKER: SAME EXISTING CHATGPT NORMAL CHAT WHICH COMPLETED EXECUTION 009. NEVER CODEX. NO NEW CHAT REQUIRED.

## 0. TASK GOAL, PRIORITY, NON-GOALS
Goal: Break the repeated model-only loop by actually attempting an AUTHORIZED, disposable PostgreSQL+Redis environment; validate and extend the source-importable EX009 harness so it exercises ACTUAL product dispatchDirective() CAS-candidate, worker boundary and transactional release fencing; run and report precisely as supported. Commit the smallest product repair only when the relevant critical integrity gates, verified HEAD and single-writer conditions pass.
Non-goals: fake green CI, create new branch, silently provision a paid cloud resource, use production services, falsify TSA witnesses or claim full production E2E from probe-Worker tests. Continue READY audit work if the integrated runtime is truly inaccessible.

## 1. CANON, LIVE HEAD AND CROSS-CHAT FENCE
Product: goif74945-crypto/NEXY.AI- ; ONLY NEXY.ai branch.
Verified product HEAD at this command's source review: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08.
Product dispatch source Git blob: 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
Product tick source Git blob: 517614809c8cefa3e516348b1268f6dca4a744e5.
Product run-state source Git blob: e162efc8b2a45014bcefbd60dc67a95d8a1e1003.
Control: goif74945-crypto/AI-CONTEXT ; ONLY main branch.
Verified control HEAD for EX009 report at source review: 5bd3f3eacc541205419045a4544e34ac3d0657b2.
These are observational snapshots only. REQUERY current branch heads, changed paths and exact blobs before planning a write, before each mutation, and before closing. If concurrent chat changes source, mark stale candidates and recompute from fresh state, never force/overwrite.
Spec: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx ; required SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
P9844 DOC-C governs BUILD, P9845 DOC-E governs DEPLOY. P9946 queue TTL 900000, P9947 max concurrent 10. Do not treat nonfinal architectural design as unproven mandatory DOC-C queue TSA checks.

## 2. READ EXACT EX009 ARTIFACTS, DO NOT REPEAT 009 AS 010
From current AI-CONTEXT/main:
- TASKS/20261008-NEXY-EX009-CROSSSTORE-CANDIDATE-AUDIT.md
- EVIDENCE/20261008-NEXY-EX009-CROSSSTORE-CANDIDATE-AUDIT.md
- EVIDENCE/20261008-NEXY-EX009-CROSSSTORE-CANDIDATE-AUDIT-candidates.md
- TESTS/009/README.md
- TESTS/009/docker-compose.yml
- TESTS/009/ex009-crossstore-pg-redis.mts
- TESTS/009/ex009-cage-failclosed-source.test.ts
- EVIDENCE/20261008-NEXY-EX009-CI-E7-ATTEMPT2-OBSERVATION.md
- verified patch provenance from 008 and invalid old patch correction in 008.

Three source-base-compatible but distinct candidates (all source-grounded at blob 002eef253... and G3 UNTESTED):
A: EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas-FIXED.patch blob b7c9444d4348fd84691cea287c9477e6c90dd734 -> expected source blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af, its own RED 5 fail 4 pass, GREEN 9/9.
B: EVIDENCE/20261008-NEXY-008-CROSS-QUEUE-REDGREEN-FENCED-queue-cas.patch blob 3296992af5276641046accc5941ed595008b63e3 -> 94340b7a591e2961b03591780668352ade165394, its own 009 RED 5 fail 4 pass, GREEN 9/9.
C: PATCHES/008/queue-dispatch-cas.patch blob 4236bcf95a1541065053d9c77d0558f923523537 -> 4610dd2d0da5aee7f1cc525b83b0815eef11fb29, its own RED 5 fail 5 pass, GREEN 10/10.
The original uncorrected A patch blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8 is INVALID (missing EOF newline). NEVER USE. Do not mix patch A with test B or cite G3 PASS based on a Vitest mock.

## 3. INDEPENDENT SOURCE OBSERVATION: EX009 HARNESS IS NOT THE DISPATCH PATCH E2E
Actually inspected TESTS/009/ex009-crossstore-pg-redis.mts (Git blob 3973fa0fae81c385b1f93617e66c2f67c8358c39), README (1971c4a190242494f0161767cdc7a507be8487f0), compose (0bfb9a705ba10b984de1b43fa7c8884919a27a9b).
The script uses real Prisma + direct BullMQ queue.add + a deliberately simplified probe Worker; it calls actual product claimDirectiveDispatch(), cancelDirectiveDispatch(), completeDirectiveDispatch(), release functions, BUT DOES NOT CALL actual production dispatchDirective() that is the CAS patch target, nor the full packages/queue/workers.ts production processJob. A hand-coded Prisma CAS in the harness is not proof that candidate A/B/C succeeds across live DB and Redis. EVEN IF EX009 T00/T01/T04/T06/T07/T11 PASS on services, label this BOUNDARY_INTEGRATION, not PATCH_E2E or PRODUCTION_WORKER_E2E.
Also inspected actual run-state.ts: its transactional commitAuthorizedPipelineRelease performs hash, LAW, run state and canceled-dispatch checks, including assertDispatchNotCancelled inside transaction (source lines 53-66 and around 258). This is an enforcement candidate, NOT cancellation-vs-release serialization proof. Test race and receipt logic, not just a static source assertion.
Do not mock TSA signatures in production. A clearly marked, authorized TEST-ONLY time injection or bounded adapter may be used only if consistent with existing tick.ts testing contract, with no claim of actual signed TSA witnesses. Distinguish clock/security boundary tests from E2E dispatch state-machine tests.

## 4. RUNNER CAPABILITY RESOLUTION: ACTIONS FIRST, NOT A PLAN
Prior worker reported authorized Windows host Node 24, npm 11, no Docker, Podman, WSL working, psql, redis-server; Linux apt update timed out; CI pre-step failures. These are HISTORICAL negative observations, not proof NO SAFE RUNNER exists now.
(A) Discover real available tools/hosts from THIS chat. Read-only query connected desktop/remote terminal, existing self-owned Codespace/dev environment, authorized CI services or container runner and their permissions. Check command -v docker/podman/psql/redis-server, existing service endpoints, OS, disk and networking with safe non-mutating probes, do not invent output.
(B) Never create paid Railway/Neon/cloud databases or modify account billing without explicit user approval. If an already-authorized disposable local runner supports services, use exact isolated compose/Testcontainers or separate native binaries with explicit loopback-only ports, fresh DB and dedicated Redis namespace, fixed independent credentials only for local disposable test, volumes not shared with other projects, no production tenant data. May perform bounded local setup under existing authorization; never change laptop system settings/enable virtualization/install untrusted executables/remove unknown volumes. Never create paid Railway/Neon/cloud databases or modify billing without explicit user approval.
(C) Verify provisioned services actually answer connections, Redis AOF and fsync, PostgreSQL schema is migrated to disposable database, cleanup targets exactly your unique resources. Record validation+cleanup. Avoid a destructive broad Docker cleanup or accidental git reset of a shared checkout.
(D) If ALL currently-authorized paths cannot run services, record each ATTEMPTED command, exit, blocker and alternative. Freeze only real-PG/Redis path, continue safe and meaningfully novel work: build a runnable product-importable source-linked producer+probe-worker test with exact fixtures and assertions, OR audit a distinct independent subsystem with source+tests, plus bounded cage fail-closed regression candidate. DO NOT re-run identical mock 9/9 or reproduce old blocked preflight as if progress.

## 5. UPGRADE TEST HARNESS, PROVE PRODUCER PATH
Design the smallest tests that import actual packages/queue/dispatch.ts from the chosen separately patch-applied isolated checkout, use REAL Prisma operations against a dedicated PostgreSQL DB and ACTUAL Redis/BullMQ for enqueueDirective(), not a copy of the updateMany code. Use controlled barriers that wrap well-defined dependency boundaries without rewriting production transitions. The intervention must preserve behavior and clearly label instrumentation/mocks, and cannot supply forged production TSA authority.
Test at least:
G3-P1: with PENDING row, publish to Redis then OWNER cancel before producer CAS => durable CANCELLED stays CANCELLED, attempts and lastError unaltered, BullMQ delivery safely ignored/removed, provider count zero.
G3-P2: Redis enqueue rejected or timeout, OWNER cancelled => no stale FAILED overwrite. Ambiguous timeout-after-publish handled as unknown side effect, not "Redis never published".
G3-P3: BullMQ probe claims PENDING before producer CAS, then producer loses to PROCESSING => no status rewind or double attempts, provider side effect respects later cancel.
G3-P4: two producer/reconcilers / one jobId => duplicate idempotency safe, authorized safe FAILED retry and maxAttempts.
G3-P5: after publish but CAS database exception, detect live Redis job and establish safe recovery behavior; no product output without LAW. Transactional release after OWNER cancel must reject with correct CANCELLED reason, and check audit/outputs.
G3-P6: restart/crash side-effects within window, can re-drive safely with durable records.
G3-P7: cancellation racing transactional LAW commit must be serialized/fenced, not only sampled before check; prove final release receipts cannot be emitted by a cancelled directive according to documented ordering. Use real tx control; do not assert impossible linearization order without a spec.
Keep distinct labels: EX009_BOUNDARY_REAL, EX010_PRODUCER_REAL, EX010_PROBE_WORKER_REAL, EX010_PRODUCTION_WORKER_REAL (only if full real worker process tested), TEST_ONLY_TIME_INJECTION, TSA_SIGNATURE_VERIFIED only if authentic witnesses verified. The required test scenario must match claimed proof depth.

## 6. CANDIDATE SELECTION AND PRODUCT COMMIT GATES
First produce evidence-backed CANDIDATE_DECISION: exact blob+patch, actual executed red/green on candidate, test import mapping, source contract vs DOC-C, state transition semantics, retries and idempotency, side effects/rollback. Candidate C has extra PROCESSING early return & lastError CAS guard; not automatically superior, must assess both compatibility and observed behavior. Do not select based on mock count alone.
Require:
- S1: fresh product HEAD/blob + safe isolation.
- S2: patch apply clean; actual exported product test RED before, GREEN after; full relevant regression + backend typecheck.
- S3: real integrated Postgres+Redis TESTED with production dispatch producer, at least the required negative cancellation/ambiguous side-effects, worker claim and release fencing. If partial service suite, report precise exclusions and do not call S3 complete.
- S4: security/time no fabricated TSA, safe queue TTL, no weakening isolation, no secret/tenant problems.
- S5: single-writer fast-forward commit only to NEXY.ai when current HEAD again matches proven candidate and all required gates for risk level pass. Commit source+tests atomically, read back GitHub files and new HEAD, re-run HEAD-bound checks where feasible. No deploy and no DOC-E release claim.
- If any critical S3 NO, leave risky product mutation FROZEN and persist test+patch in AI-CONTEXT with NOT_RUN; independent READY work continues.

## 7. CAGE, CI AND RELEASE
CAGE: EX009 source-contract negative RED old 1 fail / GREEN candidate 2 pass for bwrap fail-closed at candidate cage blob 0574ff2cd21e8ab4648c3a514dbe118446f0a949. Test inspects textual order; it does not execute Linux namespaces, cgroups or apply BPF/seccomp. Do not claim sandbox complete. Build executable Linux negative tests if runner exists, otherwise record source-contract only and assess dev/prod callsite gating without inventing policy.
CI: we independently rechecked E7 GitHub run 37741650376 attempt 2 at product HEAD 44bcb851, conclusion=failure, six jobs, latest real Redis job 113320413296 has steps=[], runner_name="" and no artifacts. GitHub created/run timestamps aren't Core time. No source test assertion failure proven, CI infra root cause UNKNOWN; check runner/job failure annotations/logs or repo workflow validation if accessible. Avoid repeated rerun loops that produce identical pre-step failure unless a specific hypothesis/testable config change is authorized. No billing/secrets/settings/protection changes.
DOC-E deploy/release remains NOT_AUTHORIZED without genuine human approvals, monitoring, rollback and current-head CI tests.

## 8. REQUIREMENT AUDIT AND LEDGER
Revalidate 98 requirement IDs via DOC-C authority and exact source+test evidence. Execution 009 15/98 audited to mixed depth and 83 NOT_REASSESSED, NOT completion=15.3%. Carry historical notes only as context, not current-head verified. Audit a new READY subsystem if integrated runner blocked; prioritize concrete semantic diff rather than more labels.
At task close: Freeze live HEAD, reread temporary in-task memory/notes start-to-end, dedupe requirement IDs, reconcile conflicting record versions (e.g., 008 patch candidates), check proof HEAD/blob, recheck bounded negatives, identify missing records, and publish full per-system table with AUDIT_COVERAGE vs ASSESSED_COMPLETION_PERCENT as separate denominators. NOT_VERIFIED isn't success or failure.

## 9. PERSISTENCE / VERIFICATION / OUTPUT
Write sanitized AI-CONTEXT/main artifacts tagged EXECUTION-010:
TASKS, LEDGER, CASES, FAILURES (blockers), EVIDENCE (test commands/exits/raw sanitized logs/source SHA), new TESTS and PATCHES if developed, with immutable provenance, latest HEAD and rollback. Read back each from GitHub and verify hashes/paths; on failure output AI_CONTEXT_WRITE_FAILED plus complete import package. Never claim work remains running after this response or claim real test result not executed.
Final required:
MODE / STATUS / PRODUCT_HEAD_START_END / CONTROL_HEAD_START_END / RUNNER_CAPABILITY_ATTEMPTS / EXACT_ARTIFACT_PROVENANCE / TESTS_ACTUALLY_EXECUTED / EX009_BOUNDARY_REAL / EX010_PRODUCER_REAL / EX010_PROBE_WORKER_REAL / EX010_PRODUCTION_WORKER_REAL / TSA_TEST_FIXTURE_AND_AUTHORITY / NEGATIVE_QUEUE_OUTCOMES / RELEASE_FENCE / CAGE_ISOLATION / CI_ATTEMPT_2 / CANDIDATE_SELECTION / PRODUCT_COMMITS_FILES / AI_CONTEXT_COMMIT_READBACK / PER_SYSTEM_98_ROWS / AUDIT_COVERAGE / ASSESSED_COMPLETION / RISKS / NEXT_READY_ACTION / VERDICT.
No mere ACK, no invented runner, no fake security certification; begin tool-based work NOW in SAME normal ChatGPT conversation.