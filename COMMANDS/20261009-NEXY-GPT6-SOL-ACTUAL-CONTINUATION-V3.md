# NEXY::GPT6-SOL-ACTUAL-CONTINUATION-V3
ROLE: EXECUTING BUILDER (a DIFFERENT chat is Independent Auditor)
MODEL: GPT-6 Sol when available; model selection cannot extend tool/session lifetime
MODE: ทำ / EXECUTE_NOW / NORMAL_CHAT / HEAD_FENCED / REAL_TESTS / ACTIVE_CYCLE
PRIORITY: FIX THE FALSE STOP AND ACT ON EXISTING CURRENT SOURCE FIRST.

## 0. OVERRIDE V1/V2 NONEXECUTION FAILURE
V1/V2 are incomplete if a builder returns "LOCAL REPAIR VERIFIED, PRODUCT COMMIT FAILED" and stops without independently checking other real GitHub write routes, without running matching Vitest/consumer tests, and without moving to other READY work. This V3 supersedes all voluntary stopping clauses of earlier command versions. DO NOT issue a final answer after ONE mini-cycle while tools and other safe READY actions remain. A report, patch ZIP, AI-CONTEXT checkpoint or "blocked" status is not an engineering completion.
Required live-session FSM:
HEAD_CHECK -> SOURCE_AND_SPEC_READ -> RUN_RED -> IMPLEMENT -> RUN_GREEN+DEPENDENT_REGRESSIONS -> WRITE_PRODUCT_IF_SAFE -> READBACK -> UPDATE_CONTROL -> RECHECK_NEXT_READY -> ACTUAL_NEXT_TOOL_CALL.
If a tool fails: CAPTURE ERROR -> DISCOVER TRUE PERMISSION -> ALTERNATE TOOL -> RETRY ONCE IF CHANGED CONDITIONS -> IF STILL BLOCKED, MARK JUST THAT ACTION -> ACTUAL_NEXT_READY_TOOL_CALL.
No fake endless loops. A standard chat CANNOT secretly execute after it responds or when its tool/session budget ends. If all calls become impossible, record a structured RESUME_HANDOFF with actual exit reason. For real cross-session automation, a genuinely authorized external scheduled worker/CI/automation is necessary and its ID and logs must be verified before claiming continuous operation. A builder is not allowed to assert that a prompt guarantees zero bugs.

## 1. READ LIVE AUTHORITY AND WORKER ARTIFACTS
PRODUCT: goif74945-crypto/NEXY.AI- ONLY BRANCH NEXY.ai.
Last known HEAD 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992. Re-query LIVE HEAD before EACH proposed Product mutation; this is not an immutable write base.
CONTROL: goif74945-crypto/AI-CONTEXT ONLY main, last known at beginning of this forensic audit 39698363a74bc82bd4fdfe9c48c019c0a8abc8b2; re-query.
AUTHORITATIVE SPEC "แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx", expected SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7. Source the ACTUAL bytes and hash; section/paragraph and schema decide behavior, not worker narrative.
Worker's previous execution report is untrusted until independently proved. It claimed:
- original canonical JSON RED 5 PASS / 5 FAIL, patched 10/10 GREEN, standalone tsc PASS and patch applies;
- 5/5 current-head attestation tests PASS;
- Product commit REJECTED; AI-CONTEXT write REJECTED; bundled ZIP allegedly exists;
- no real full-repository Vitest or CI at patched HEAD.
DO NOT elevate this to PRODUCT_FIXED. Search its ZIP/test/patch/logs in actually accessible current conversation attachments, project files, authorized shared library, GitHub/AI-CONTEXT; inspect manifest, sha256, git patch --check and source. If the ZIP exists only in another chat and cannot actually be read here, record ARTIFACT_NOT_ACCESSIBLE, then reproduce a minimal correct patch against current source and TEST it. Never invent the ZIP's contents or a sandbox path.

## 2. LIVE FORENSIC FACT: GITHUB WRITE BACKEND IS NOT GLOBALLY UNAVAILABLE
Independently observed at time of V3 audit:
- Repo Code Bridge runtime_status: github_api_connectivity=CONNECTED; read_backend_status=READY; write_backend_status=READY; ci_backend_status=READY; gateway_write_policy=ALLOW; D1 READY.
- Repo Code Bridge repo_status(goif74945-crypto/NEXY.AI-, branch=NEXY.ai): HEAD 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992; permissions_actually_verified pull=true, push=true, admin=true, read_only=false. This establishes a reported CURRENT CAPABILITY, NOT a guarantee that any particular commit will succeed. Repo Code Bridge repo_search once timed out 504, which alone is NOT denial of repo_write.
- Separate GitHub connector offers fetch_file, update_file, create_file, create_blob, create_tree, create_commit, update_ref with expected_sha/force=false. In earlier EX012, this GitHub connector actually committed the independent LAW patch; therefore there is a proven alternate class of route, although live permission may change.
- NEXY.ai current canonical file packages/core/canonical-json.ts Git blob 3894381cc80648c31f38b7b88035a64ee1d9cde6, existing canonical contract tests tests/contract/canonical-json.test.ts blob 688d317063ec7201c1a2ee7815685d3caeb3de18. These old blobs must be checked against LATEST HEAD before patching.
- Current broad CI exact-head run 37819115867 failed with job steps=[] and runner_name="" (root cause not proved). Do not conclude code caused a job that never started.
- Remote Desktop Commander DESKTOP-FOB7IK8 last observed Offline. Tool-specific state, not global engineering inability.

MANDATORY WRITE ROUTE ESCALATION:
W0. GitHub FETCH live NEXY.ai HEAD and exact touched file blob. Revalidate content/byte checks and branch allowlist.
W1. Repo Code Bridge runtime_status -> repo_status -> prepare_change_set (path, expected_revision, idempotency key) -> commit_change_set (fresh head, idempotency key). Capture actual error verbatim and inspect status of prepared change set before retry; no duplicate commits.
W2. If W1 FAILS, use native GitHub connector create/update file with current SHA for minimal text-only patch; for atomic source+test use create_blob -> create_tree(base actual HEAD tree) -> create_commit(parent exact HEAD) -> update_ref(branch=NEXY.ai, expected_sha exact HEAD, force=false). A successful create_commit alone is NOT a branch commit. Do not claim success before branch and blob readback.
W3. If W2 genuinely denied by GitHub permissions/protection, inspect exact HTTP/status/ruleset, allowed PR/CI path and connected authorized repository editor. Do not create unauthorized extra Product branch. Save tested patch+test under AI-CONTEXT/main if this path is writable.
W4. If all write routes fail in this live session: record EVERY route/error and freeze only Product mutation. Continue code audit, source-linked tests, DOC-C requirement extraction, and Railway/CI source diagnostics. Never finish solely because product write was refused once.
Never force-push, delete branches, modify protection, impersonate authorization, expose secrets or overwrite concurrent changes. A different live HEAD means read diff, reconcile conflicts, rerun tests on new HEAD.

## 3. FIRST TASK: COMPLETE THE EXISTING CANONICAL JSON REPAIR
Read packages/core/canonical-json.ts and all 13 GitHub code-search references. The current code uses value.map(...).join(",") for arrays (can skip sparse slots), Object.keys(record).sort() and record[key] for objects, and does not test object prototype/cycles/symbol own keys/getter descriptors. Test actual observed contract and callers.
SOURCE_RELATED_CALLERS (seen on exact HEAD):
- packages/api/directives.ts uses sha256hex(canonicalJson(body)) for idempotency request hashes.
- packages/api/owner-roles.ts uses canonicalJson for OWNER role-change requestHash.
- packages/api/live-config.ts uses canonicalJson for runtime config update and rollback requestHash.
- packages/api/cold-snapshot.ts uses canonicalJson for cold-snapshot contentHash and requestHash.
- packages/config/runtime-config.ts uses canonicalJson in recursive configuration diff.
- tests/contract/canonical-json.test.ts asserts canonical nested ordering, primitives and unsupported type failures.
- tests/contract/determinism-boundary.test.ts expects canonical request fingerprints.
DON'T blindly accept the worker patch: inspect actual patch before applying, error and schema compatibility, and all relevant callers.
REQUIRED NEGATIVE CASES: sparse array (hole at 0 or middle), array with extra enumerable properties or symbol properties, Date, Map, Set, class instance, cyclic array/object, symbol-keyed record, getter and accessor with side effects, undefined/nan/infinity, unsafe keys that require JSON escaping, nested array/object, stable key order; reject unsupported JSON-domain values without throwing unrelated process-level side effects. Inspect Proxy/toJSON risks; document any nonprovable safe behavior rather than falsely claiming total purity.
REQUIRED POSITIVE: primitives, plain object, empty object, nested deterministic key ordering, arrays including undefined? NOTE: canonicalJson current contract expressly rejects undefined; preserve that. Repeated references that are acyclic should remain valid if original semantics allow. Verify parser JSON.parse output matches expected normalized content for supported domain.
REQUIRED STEPS: original current HEAD RED test result on real checkout; smallest safe code change; actual TypeScript and Vitest targeted GREEN; relevant consumer regression, broad tests where runner exists; classify unrelated preexisting red tests; verify exact source/test blob and package boundaries. Never weaken existing contract/determinism tests to pass.
IF "standalone test passed" only, do NOT commit without checking equivalent real repository Vitest and caller tests when executable. If one runner unavailable use Linux/authorized CI or another real runner; continue independent scope simultaneously.
ONLY commit Product source+regression through W1/W2 after required proof, then verify NEXY.ai branch HEAD, exact changed paths and blobs and test status. If patch is not ready, continue tests/callers and next spec requirement.

## 4. SECOND+ READY WORK, WITHOUT ENDING AFTER CANONICAL JSON
Candidate queue already observed from live original sources; refresh live before selecting:
A. Current-head attestation: previous worker asserted 5/5 PASS, but evidence must tie to current HEAD; read last commit tests/contract/current-head-attestation.test.ts at 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992.
B. Rust cargo/const-depth: earlier broad Windows 905/911 (six failures included cargo missing and tier depth). Use real Linux Rust runner to distinguish environment from logic. Never claim Rust tests passed if cargo isn't run.
C. Railway NEXY Validation R2 project 01537473-6a6d-42a0-856f-40d8a4e6a712; existing validation service pinned OLD 9e615b04... and old build failures. Re-query project/service/deployment logs, isolate TEST-ONLY resources before running against any database/Redis. Resource quota refusal to create a new project must not stop read-only log investigation, GitHub CI or local source tests. Do not run destructive test on production-named DB without proven disposable schema + authorization.
D. Real Queue/BullMQ/Postgres/Redis G3 current-head tests, if and only if isolated tested database and worker runner are authorized; otherwise freeze G3 action and implement/test another deterministic module.
E. Current-head CI runner failures with steps=[]; investigate actual workflow run jobs/source and resource permissions without guessing the cause.
F. DOC-C/DOC-D atomic requirement inventory beyond historical 98 tracking slots, UI semantics, 12 canonical routes, 14 named UI components and DOC-E E1-E12 separate release proofs. Select source-linked READY missing feature and implement+test, not just tabulate.
G. Other actual source defects discovered by real static/negative tests. Do not invent missing features.
Choice algorithm: pick highest-risk VERIFIED_READY task, or most informative executable READ_ONLY action if no safe mutation exists. Continue immediately to it after prior cycle; do not respond final after one local patch.

## 5. AUTONOMOUS FORWARD-PROGRESS GATE
Track CYCLE_COUNTER, START_HEAD, ACTIVE_TASK, TEST_RESULT, WRITE_ROUTE_USED, LAST_SUCCESSFUL_COMMIT, ALT_RUNNERS_TRIED, NEXT_READY_ACTION, SOURCE_HASH and OUTSTANDING_ATOMIC_REQS in actual temp memory/AI-CONTEXT.
After every action group:
1. Capture actual tool/command/exit. If no new tool output, no engineering progress has occurred.
2. Re-evaluate Ready queue for all other subsystems, not only current one.
3. If any safe READY action exists AND tools are responsive, CALL ITS TOOL before issuing a final answer.
4. If a permission blocks one action, search existing specific authorization; if absent freeze ONLY it. Don't bypass security/production/billing. Continue with a different action.
5. If a plugin connection times out, use other connected plugin; do not fabricate tools or assume no alternate.
6. Write sanitized TASKS/LEDGER/CASES/FAILURES/EVIDENCE/ATOMIC_MATRIX/RESUME_CHECKPOINT to AI-CONTEXT/main with readback. A successful checkpoint is NOT terminal when work remains.
7. End a live turn only when actual platform/runtime limits prevent further tool calls, or ALL safe READY work truly exhausted with evidence, or ALL accepted requirements proved; include exact STOP_REASON and peer-review handoff. There is NO text-level mechanism to force a chat to execute after the final reply. To run autonomously across sessions, configure a real authorized scheduler/CI/automation with runtime, scoped credentials, budget, concurrency lock, error handling and rollback, and prove job ID and actual run before claiming 24/7. Do not configure unapproved billed/destructive infrastructure.
8. Avoid continuous retry of the identical denied request; a state change/new tool/new scope is required.
This is an active-session transition contract, not a claim of unlimited autonomous runtime.

## 6. COMPLETENESS, TESTS AND LAW GATES
Atomic matrix must enumerate all *mandatory* spec requirements including DOC-C and applicable DOC-B/D, and separately DOC-E E1-E12 for release. Use real DOCX bytes, sha256, exact paragraph IDs; preserve contradictions and exclude explicitly future/experimental items from current denominator only when source supports it. Historical 98 rows are coordination entries, not all spec features.
Track by EACH system/feature: SOURCE_LOCATOR, ACCEPTANCE, CURRENT_BLOB/HEAD, real tests+exit, negative security, changed code, status VERIFIED/FIX_REQUIRED/NOT_VERIFIED/OUT_OF_SCOPE, confidence and freshness. Audit coverage != feature completion != tests pass %. Do not count NOT_VERIFIED as 0 or 100. No overall percentage if denominator not proven exhaustive.
Tests needed depending on scope: unit, contract, integration, Rust, CI head-bound, real worker+Postgres+Redis, race/retry/idempotency/cancellation, auth/RBAC/tenant, prompt injection, sandbox, rollback, UI/accessibility. Source presence cannot prove runtime PASS.
Do not merge DOC-E deploy/production authorization into build/test permissions. Search for recorded applicable signoffs before marking missing; NEVER invent signoffs or manipulate live production beyond in-scope permission.
Independent AUDITOR approves or rejects evidence, not builder.

## 7. FINAL OUTPUT ONLY AT A GENUINE BOUNDARY
MODE | CYCLE_COUNTER | STOP_REASON(T1/T2/T3 with proof) | PRODUCT_HEAD_START/END | CONTROL_HEAD_START/END | ORIGINAL_SPEC_SHA256 | CANONICAL_JSON_PATCH_SOURCE_SHA | PATCH_TEST_SHA | TOOL_CAPABILITIES/ERRORS | RED GREEN VITEST AND TYPESCRIPT REAL EXITS | CALLER_REGRESSIONS | RAILWAY PROJECT/DEPLOYMENTS + ISOLATION | G3 | CI HEAD | ALL SYSTEMS/FEATURE ATOMIC MATRIX + AUDIT COVERAGE vs COMPLETION | ALLOWED WRITE ROUTE USED + COMMIT READBACK | ALL UNRESOLVED TASKS | NEXT_READY_ACTION + EXACT TOOL CALL | AI-CONTEXT files + readback | VERDICT.
At the very start DO THE FOLLOWING (not planning):
1. Call live GitHub and Repo Code Bridge repo_status and runtime_status, verify HEAD and write path.
2. Inspect worker patch files from actual accessible data; if unavailable, obtain/recreate from original source without guessing its bytes.
3. Run exact canonical JSON regression and call-site tests on real runner. Fix and commit under W1/W2 if safe.
4. Then immediately execute next READY task. Do not terminate just because first patch was done.
