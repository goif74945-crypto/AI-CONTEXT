# NEXY.AI — EXECUTION 008 | NORMAL-CHAT IMPLEMENTATION & VERIFICATION
SYSTEM: NEXY::NORMAL-CHAT-QUEUE-CAGE-IMPLEMENTATION-CLOSURE-V2
WORKER: SAME EXISTING CHATGPT NORMAL CHAT FROM EXECUTION 007; NOT CODEX; NO NEW CHATS
MODE: ทำ | EXECUTE_NOW | CROSS | EVIDENCE_DRIVEN | SINGLE_WRITER | FAIL_CLOSED | NO_GUESS | IMPLEMENT_TEST_VERIFY

## 0. IMMEDIATE OBJECTIVE
Continue in THIS already-working normal ChatGPT chat. Do substantive engineering rather than another unchanged risk recap. Priority: (1) obtain real executable test capability or establish bounded infrastructure blocker; (2) reproduce and repair QUEUE-CANCEL-RACE-006 with product-integrated regression and Redis/DB side-effect safety; (3) investigate/enforce cage isolation fail-closed boundary; (4) make further real requirement audits/repairs where independent.
Do not hand off to Codex, open additional chats, claim access to browser/dev tools not actually connected, or promise background continuation.
A PARTIAL outcome is acceptable only with specific new verified engineering artifacts, including runnable product-integrated test/patch evidence or a distinct completed READY repair; repeating previous model/source findings alone is NOT task progression.

## 1. SOURCE OF TRUTH, FENCING, CONCURRENT WRITERS
Product: goif74945-crypto/NEXY.AI-; ONLY branch NEXY.ai
Last VERIFIED product branch HEAD at instruction creation: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Coordination: goif74945-crypto/AI-CONTEXT; ONLY branch main
Last VERIFIED control HEAD before this instruction was authored: fc7dc9570cbe2d3a9a287db1c2613b1f97739cb7
These heads are OBSERVED snapshots, never unconditional write bases. Re-fetch live branch HEADs before implementation, before every mutation, and at close. Check and handle HEAD drift or conflicting source blob IDs; no force, reset, branch create/delete or overwriting other chat commits.
Authoritative DOCX: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
Required SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
DOC-C P9844 controls BUILD; DOC-E P9845 controls DEPLOY. Hash the source in your OWN chat if actually available; earlier matched hash is proof only of earlier verified artifact, not automatic new-byte access.
Read at live control main:
- EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS.md
- EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS-model.test.cjs
- LEDGER/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS.md
- CASES/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS.md
- FAILURES/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS.md
- COMMANDS/20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007.md
Bound previous verified model-only results to earlier HEAD; never reinterpret as production integration.

## 2. INFRASTRUCTURE AND RUNNER REALITY FIRST, NOT AN EXCUSE TO STOP
Tool capability matrix: identify, invoke where appropriate, and record exact read/execute/write/runner privileges for all currently CONNECTED services (GitHub, Repo Code Bridge, authorized development host or remote desktop/terminal, already-available isolated test runner, etc.). Tool list visibility is not proof of connection. No unauthorized access, secret requests, billable hosting provision or production DB use.
Search repo package.json, test scripts, Docker Compose/testcontainers fixtures, Prisma schema/migrations and lockfiles for the MINIMUM actual test commands and prerequisites.
Inspect current HEAD GitHub Actions run/job logs and workflow definitions before editing workflows. At observed HEAD 44bcb851:
run 37741650349 exact-head-evidence, 37741650343 deploy, 37741650376 E7 queue, 37741650355 cargo lock, 37741650318 six-system all have GitHub "failure" on PUSH.
Additional verification from this command-authoring chat: 37741650349 has job 113193487317 runner_name="" and steps=[]; E7 run 37741650376 has six jobs with runner_name="" and steps=[]. These prove PRE-STEP execution failure for those jobs, NOT the underlying cause. Inspect run/job logs/check annotations/workflow validation/runner provisioning status using authorized readable APIs. Do not guess billing, policy, YAML or quota; if inaccessible write "ROOT_CAUSE_UNKNOWN" and targeted evidence needed. Repo Code Bridge ci_dispatch 403 REPOSITORY_READ_ONLY is a denial by that endpoint only, not a blanket GitHub write/runner verdict. No fake rerun claimed.
If a safe authorized isolated runner is available: execute focused tests, real Postgres/Redis integration, isolation negative tests. Capture command, exit code, stdout/stderr (redacted), environment versions, commit HEAD and actual assertion counts.
If none: STOP claiming runtime validation; independently prepare REAL repo-integrated tests and a precise minimal source patch, store under AI-CONTEXT and annotate NOT_RUN. Continue safe source/code audit of another READY subsystem. Do not commit high-risk product fixes that require integration verification if the required tests cannot be executed.

## 3. QUEUE-CANCEL-RACE-006 — FIRST IMPLEMENTATION TARGET
Observed exact source at product 44bcb851:
- packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29, lines 110–182: dispatchDirective loads durable row; awaits enqueueDirective; unconditional prisma.directiveDispatch.update where only id changes status to ENQUEUED, or FAILED in catch.
- cancelDirectiveDispatch lines 301–319 conditionally writes CANCELLED.
- packages/queue/jobs.ts blob e90ac64acc446c5bbd24a710e0208fc76bce9089: BullMQ idempotencyKey as jobId; queued item may exist even if later DB state transition conflicts.
- packages/queue/workers.ts blob 3134e7b6bf83f7200959e3e267b28f5ea28b6392: claimDirectiveDispatch guards PENDING|ENQUEUED, cancellation watch and later release fence require verification.
- packages/queue/retry-policy.ts blob 3888169fc88784c999c31ff0f19ad673ba0e0f11: only explicitly safe retry code QUEUE_UNAVAILABLE.
These are point-in-time blob IDs; re-read and compare before patch.

Actions in order:
Q1. Enumerate exact FSM, retry policy, affected row selectors, TTL producer/consumer, schema constraints, and every call site. Include cancellation API and downstream pipeline run final-release transaction.
Q2. Move earlier standalone 5-test JavaScript model into a REAL product-linked regression harness using repository test framework. The source-integrated tests must invoke actual exported dispatch/reconcile/claim/cancel functions or an isolated faithful test boundary; tests that copy/paste replacement logic into a fake function are only models. Maintain separate labels MODEL, MOCK_INTEGRATION, POSTGRES_REDIS_INTEGRATION.
Q3. Use controlled barrier/deferred promises to prove original bug (cancel while enqueue pending and during error) and capture failing test BEFORE source fix. Also test cancellation before enqueue and after Redis job creation.
Q4. Design smallest coherent correction, NOT blind copy-paste: optimistic compare-and-set state+attempts (conditional updateMany) around post-await outcome may prevent status resurrection; keep catch limited to actual enqueue failure so CAS conflicts cannot fall through and overwrite status as FAILED. On CAS.count=0 re-read durable row; never increment attempts/reset lastError/resurrect CANCELLED, COMPLETED or PROCESSING. Return accurate delivered/idempotent results and failure classifications. Guard FAILED explicit retry allowlist and maxAttempts.
Q5. Cover cross-store window: Redis enqueue can succeed BEFORE DB CAS. Establish whether worker is permitted to claim a PENDING row, how CANCELLED prevents provider execution, what reconciler does, and whether Redis stale job must be deleted or safely ignored after losing CAS. Avoid unsafe deletion that could remove a legitimate job. Prove correctness under duplicate workers, crash/restart, cancellation during SWARM, and durable output-release gate. If two-phase outbox is needed, first prove it compatible with DOC-C and schema; prefer minimal reliable solution.
Q6. Tests: success/cancel; error/cancel; cancel before/after BullMQ publish; duplicate producer/reconciler; FAILED retry only with authorization; exhausted attempts; cancellation during PROCESSING; old worker claim PENDING; Redis unavailable; DB failure; crash after publish before durable transition; no unauthorized provider invocation; no forbidden output release. Assert durable DB final status, BullMQ state, attempts, audit, idempotency and release receipts. Run isolated REAL Postgres + Redis for "RACE_CLOSED_INTEGRATION"; model-only pass cannot earn that verdict.
Q7. If executable environment and gate are ready: implement smallest code patch with tests, run focused tests then types/static/lint/integration, current-head git diff and commit only to NEXY.ai with optimistic expected-head fence. Read-back changed files and record new HEAD. Fail closed, no hidden error swallowing. If required test gate is unavailable: store exact diff and runnable test source in AI-CONTEXT as UNTESTED CANDIDATE, NOT product fix. Continue another READY task.

## 4. CAGE ISOLATION — SEPARATE SECURITY WORKSTREAM
Observed packages/phase-f/lo3/cage.ts blob 5afd464ed39470381ef1df643a630e1f431817dc:
bwrapAvailable false -> direct spawn in runLinuxCgroupSeccomp lines 555–566, while return labels linux-cgroup-seccomp. cgroup permission errors may be ignored; seccompJson written, no verified BPF/filter execution in examined path.
C1. Trace production use, mode restrictions and user input trust. Map DOCX isolation semantics P4137–4149 and P4886–4927 to exactly applicable runtime contract.
C2. Distinguish confirmed source behavior from exploitable production exposure. No unsupported assertions of applied namespaces/seccomp/cgroups.
C3. If protected untrusted execution requires isolation, forbid transparent direct-spawn fallback; return structured non-success "isolation unavailable" without invoking command. If an explicit dev-only mode is allowed by authoritative spec, fence and label it honestly, never accidentally enabled by prod conditions. Do not silently change backend name to make compliance appear.
C4. Run Linux negative tests for missing bwrap, namespace-denied hosts, cgroup failures, no seccomp enforcement, trusted executable with /opt dependencies, path traversal and host access. Tests MUST measure actual isolation, not only whether arguments were constructed. If no runner, put reviewed code/test patch in control repo with NOT_RUN and security status unresolved.
C5. Do not weaken sandbox, bind whole host FS, disable protections or call JSON policy an enforced seccomp filter.

## 5. TSA IS INDEPENDENT AND MUST NOT BE FORGED
DOC-C P9945–48: stale_job_ttl_ms = 900000, max_concurrent_pipeline_runs = 10. Final DOC-C explicitly requiring direct TSA signature checks for this TTL has NOT been established. Broader Core time law P5151–58 prohibits arbitrary machine-clock reads in Core and permits TSA-injected batch time; a distinct 2-of-3 time policy exists in broader architecture. Trace true production authority/injection chain before changing it; no Date.now/new Date/system time substitution in Core, no synthetic signatures/quorum. Freeze ambiguous TSA patch only, keep Queue cancellation code work independently READY.

## 6. CI, 98-ROW MATRIX, AND PRODUCT VALIDATION
If all current GitHub Actions jobs fail before steps, DO NOT modify source/test logic to make CI green. Separate infrastructure workflow/root cause report from code correctness.
Re-evaluate 98 canonical requirement IDs at current source HEAD one by one, identify original paragraph requirements, source blobs, integration paths and test proof. Report full per-system matrix, with audit coverage and assessed completion on different denominators; unknown statuses neither count as 0 nor as 100. A prior historical audit of 39/98 is NOT current-head percentage.
Only product code that passes applicable executed tests can be called TESTED. No DOC-E release authorization without real signoffs, deploy rollback drill, incident proof, monitoring and exact HEAD CI evidence.

## 7. MULTI-CHAT WRITE FENCE
One active writer per code path; cannot assume lock from mere chat agreement. On every write:
- independently requery NEXY.ai HEAD and source blob
- compare source bytes for touched files, re-evaluate planned patch if drift
- smallest independent atomic change on allowed branch, no force push/branch mutations
- read back commit and code, record test HEAD and whether final HEAD still matches tested code
- if concurrent conflict: halt that mutation, rebase concept and continue unrelated safe actions
- never expose secrets or use production credentials/data.

## 8. AI-CONTEXT TASK CLOSURE (MANDATORY)
Use distinct Execution 008 task identity and append new evidence; never rewrite historical records into "current head verified".
Write TASKS, LEDGER, CASES, FAILURES (for blockers), EVIDENCE (commands, tests, source proof, full file artifacts), plus actual patch/tests if unexecuted, into AI-CONTEXT/main, and read back each. If write blocked, return AI_CONTEXT_WRITE_FAILED with a complete import package.
Keep a temporary per-step ledger with source/claim/proof/dependency/status; at closing freeze observed HEAD, reread all records, deduplicate requirement IDs, detect contradictions, verify evidence blobs and freshness, recheck bounded negative claims, identify uncovered requirements, compute coverage distinct from completion, and clearly mark all missing tests.
No background work, invisible progress or fabricated success.

## 9. GATE TO END THIS TURN
Required distinct engineering deliverable besides recap: (A) verified product commit with executable tests and readback, OR (B) genuinely repo-linked test + exact, runnable minimal patch candidate stored in control repo if runner blocked, OR (C) distinct verifiable code-level fix for independent READY requirement with appropriate tests. A mere five-test model rerun does not satisfy.
If cannot achieve A/B/C, report precise blocked path and real, newly verified facts rather than claim progress.
Final response fields:
MODE, STATUS, PRODUCT_HEAD_START/END, CONTROL_HEAD_START/END, SPEC_STATUS, RUNNER_CAPABILITIES, QUEUE_DELIVERABLE, MODEL_TESTS, PRODUCT_TESTS, POSTGRES_REDIS_TESTS, CAGE_SECURITY_VERDICT, CI_WORKFLOW_ROOT_CAUSE_STATUS, WORKFLOW_RUNS, TSA_AUTHORITY_STATUS, PATCH_FILES, COMMIT_SHA(s), READBACK_PROOF, PER_SYSTEM_98_ROW_TABLE, AUDIT_COVERAGE, ASSESSED_COMPLETION_PERCENT, DOC_E_RELEASE_GATE, FAILURES, NEXT_READY_ACTION, VERDICT.
Use PARTIAL when verification or release requirements remain outstanding.
EXECUTE NOW, IN SAME NORMAL CHAT.