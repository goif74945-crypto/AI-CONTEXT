# NEXY::CODEX-ULTRA-DEEP-EXECUTION-AND-PROOF-V8

**MODE:** EXECUTE_NOW / MAX_SAFE_ENGINEERING_THROUGHPUT / SPEC_EXACT / SOURCE_COMPLETE / IMPLEMENTATION_FIRST / FIVE_LANE_AUDIT / TEST_INTENSIVE / ADVERSARIAL / CURRENT_HEAD_CAS / FAILURE_TRIAGE / CONTINUOUS_WHILE_ACTIVE / EVIDENCE_FIRST / NO_FAKE_PASS / FAIL_CLOSED

**MISSION:** Perform actual engineering on the authorized NEXY-IGNIS product, not an endless prompt-generation or audit-summary loop. Starting from the original SHA-verified build specification and current actual source, enumerate every in-scope atomic requirement, identify real gaps, implement the smallest complete correct fixes, generate meaningful regression and adversarial tests, execute them on exact revisions, repeat until no executable safe work remains in the active Codex execution. Produce a cumulative, verifiable closure record. **Depth is measured in verified requirements, independently exercised failure modes and safe fixes, not in token use, file count, commits, wall-clock claims or verbosity.**

This instruction DOES NOT launch Codex, create a background job, imply a 24/7 worker, or grant Product write permissions by itself.

## 00. BEFORE ANY PRODUCT MUTATION — AUTHORITIES AND VERSION FENCE

Read FIRST from live goif74945-crypto/AI-CONTEXT branch main:
- START-HERE-NEXY-IGNIS-CODEX-20261010.md (V8 is active command when published there)
- COMMANDS/20261011-NEXY-CODEX-ULTRA-DEEP-EXECUTION-AND-PROOF-V8.md (this file)
- POLICIES/20261011-NEXY-V8-HARD-EVIDENCE-AND-PRODUCTIVE-LOOP-V1.md
- POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md
- EXECUTION/20261011-NEXY-V8-88-GROUP-REVISION-BOUND-WORK-GRAPH.tsv
- EXECUTION/20261011-NEXY-V7-EVIDENCE-FIRST-WORK-QUEUE.tsv
- NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.md and .tsv
- NAVIGATION/20261010-NEXY-AI-FROZEN-HEAD-889-BLOB-MANIFEST.tsv
- COMMANDS/20261011-NEXY-CODEX-MAX-ENGINEERING-THROUGHPUT-V7.md and V6/V5 when their base contracts are relevant
- EVIDENCE/20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT-INTERIM-GATE-REPORT.md for reproducible historical leads, NOT present-day acceptance.

Read the Product goif74945-crypto/NEXY.AI- AGENTS.md at **live** branch NEXY.ai. The only authorized Product mutation branch is the EXISTING NEXY.ai. No new branch, temporary branch, hidden branch, fork branch, auto-created Codex task branch, force push, rewritten remote history, destructive reset or branch deletion/rename. Any cloud Codex environment that implicitly creates a branch must be rejected for Product writes; select a permitted in-place existing-branch workflow after independent permission verification. Existing Product branch historical anchor at command creation: 58b1200bd61b867e917057d0019eea78ea9f6b2a. Refresh before all edits, tests, commits and verification; this is not a permanent HEAD.

**Authoritative original:** แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx (or byte-identical authorized alias). Require SHA-256 of actual file bytes exactly:
b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Read the actual source text and paragraph numbering (P is one-based including blank paragraphs, NOT pages). P09837–P09845 defines authority split. DOC-B = SYSTEM LAW; DOC-C P09886–P10499 = current BUILD SPEC; DOC-D P10500–P10722 governs supported product design; storage/auth supplements require DOC-C applicability; DOC-E P10917–P10999 controls DEPLOYMENT EVIDENCE AND SIGNOFF. Historical 143 checkpoints and 88 navigation groups are aids, NOT complete atomic requirements. Resolve all conflicts using original neighboring clauses and authority; no scope expansion from early drafts, DOC-A vision or Phase-F experiments. Without verified bytes, STOP normative build mutations affected by unknown spec; independently permissible source/CI diagnoses may continue.

## 01. EXECUTION PRECONDITIONS: ACTUAL CAPABILITY AND SAFE RESOURCES

Capture as facts: current tool permissions, live HEAD, exact Git tree hash, working tree, Node/npm/Cargo and lockfile versions, memory/cpu/disk, PostgreSQL and Redis isolation, browser E2E availability, CI runner state, credential boundaries. Run commands only on an authorized local or hosted environment. Do not presume that a plugin has unrestricted write or CI dispatch rights. Do not send secrets to logs, AI-CONTEXT, paste bins, or cloud services. Database migrations must use disposable isolated DB unless separately authorized.

For constrained hardware, determine whether running concurrent tests causes swapping or timeouts; use a measured bounded concurrency cap, do not force concurrency=100. Parallelize independent read/review/test lanes, **never concurrent Product commits**, destructive DB operations, conflicting builds sharing output directories or competing npm installs. Stop expensive fuzz/performance runs when resource ceiling risks damaging workspace or altering billing. Do not spend paid compute without authorization.

## 02. BOOTSTRAP WITH EXISTING MAP: INCREMENTAL, NOT RESTARTING DISCOVERY

1. Fetch both remote HEADs. Verify Product git ls-files against full recursive Git tree. At the map's frozen source HEAD there were 889 tracked Git blobs, but current count MUST be live and complete. Inventory every tracked blob with path, mode, size, SHA, encoding/classification, full-read status and semantic-review status. Count binary/generated/symlink/submodule separately.
2. Read the V8 88-group graph. Its source/test SHA fields were verified at frozen HEAD; match them to current tree and use valid unchanged paths as lookup accelerators. If Product HEAD advanced, compute exact diff and revalidate affected paths; do NOT restart random whole-universe grep, and do NOT reuse stale behavior proof.
3. Read every applicable original DOC-C obligation and in-scope supported DOC-D/storage/auth clause. Decompose to atomic, deduplicated requirements with stable identifiers, source paragraph, expected observables, failure/negative cases, actual dependent modules, test plan and acceptance verdict. Make no claim of complete build requirement denominator until every normative clause is enumerated and reconciled.
4. For each full text file, record READ_FULL only after actual bytes were fetched; record SEMANTIC_REVIEW only after inspecting behavior, imports/callers, side effects, persistence, error paths and test coverage; mark VERIFIED only after runnable proof.
5. Persist a local crash-resumable ledger OUTSIDE tracked Product files. Record product_HEAD, control_HEAD, spec_SHA256, per-file blob SHA, per-atom state, exact commands and output digest; append superseding events instead of erasing old failures. Revalidate proof when source or environment changes.
6. Avoid duplicate review from independent agents: canonical work key = SPEC_ATOM_ID + current source blob digest(s) + affected test digest + environment class. No cross-HEAD PASS reuse.

## 03. FIVE ACTUAL WORK LANES — BOUNDED AND EVIDENCE BASED

**LANE A — Spec authority:** Original DOCX full reading, conflicting and excluded scopes, atomic requirements, acceptance predicates, authoritative paragraph and dependencies. Do not invent requirements; derive ALL obligations.
**LANE B — Source/data-flow:** Complete file inventory, functions/exports/callers, state mutations, Rust/TypeScript parity, endpoints, validation, SQL and schema, externally visible behavior; identify actual implementation gaps, not names of files.
**LANE C — Dynamic verification:** Compile/test/install in isolated exact source, focused contract/integration/E2E, disposable Postgres/Redis, worker queue, restart/replay and crash consistency, measured resource accounting.
**LANE D — Adversarial engineering:** Property-based, model-based, metamorphic, mutation-test sampling, fault-injection, malformed input, security boundary, races and timeouts. Every technique must have an actual executable test harness and logged result.
**LANE E — Repair and independent review:** Confirm RED, implement smallest complete safe fix, prove GREEN and cross-module regression, independent review of diff, atomic authorized single-writer push, exact HEAD readback and safe evidence journal.

If subagents are supported, use them only for independent read/review/test tasks. If not, execute lanes sequentially. No agent may inherit Product write authority from another chat. DO NOT claim a lane ran unless it returned actual evidence.

## 04. SCHEDULER: PRODUCTIVE LOOP, NOT REPORT-ONLY

Derive a DAG of ALL atomic requirements. Pick work by real impact: severity/security first, then ready prerequisites, reproducibility, unlocked dependencies and number of affected consumers. V7's 14 candidate tasks are leads, not confirmed defects. Avoid starting dependent UI polish before missing mandatory underlying contracts. A blocked task is local; advance the next safe independent READY task.

A FULL engine cycle:
1. LOCK current source SHA and current policy/owner approval.
2. READ exact spec paragraph plus neighbors and full current implementation/callers.
3. CLASSIFY: CORRECT_WITH_PROOF / BUG_REPRODUCED / SPEC_REQUIREMENT_MISSING / UNKNOWN / OUT_OF_SCOPE.
4. For BUG or MISSING: create minimal **RED** test (including one relevant adverse path); record its expected and actual output and pre-fix HEAD. Do not fabricate RED by making test impossible or by mocking away production behavior.
5. IMPLEMENT minimal source-correct patch at architecture-compatible layer. Follow immutable contracts, no unauthorized new API, no fake retry, placeholders, no catch-all that suppresses exceptions, no disabling gate.
6. Execute GREEN focused tests, then affected callers/integration, typecheck/lint, applicable full suite and targeted adverse/mutation tests; gather actual exit codes.
7. Review diff, blob SHA, dependencies, lockfile changes, data integrity, rollback, security invariants and resources.
8. If checks pass and authorization allows: **single-writer** Product NEXY.ai write with fresh remote HEAD CAS. If conflicting peer advancement: do not push; re-read paths, reconcile in local *unpublished* workspace, re-test, retry only after valid HEAD alignment.
9. Re-fetch Product GitHub commit and changed blobs; verify remote data and HEAD; append sanitized evidence to AI-CONTEXT/main with unique path; independent reviewer checks changed path/evidence if available.
10. Resume next READY work in active execution without repeatedly requesting user to type 'continue'.

If source is compliant, do not churn code; instead add legitimate missing verification where demanded, or move on. If no safe path to commit, create runnable isolated patch and mark PATCH_READY_NOT_MERGED. A change-only count NEVER equals productive progress.

## 05. HIGH-INTENSITY TEST PROTOCOL (ACTUALLY RUN, NOT JUST DESIGN)

**Static + compile:** Contract/scope and module boundary checks, TypeScript backend/web, Rust workspace toolchain with Cargo.lock, npm lock determinism, Prisma schema and migration pair integrity, lints, forbidden imports and nondeterministic authoritative behavior.

**Positive + negative integration:** Exact API validation, auth/OTAC replay and lockout, rate limiting, session/device binding/CSRF, OWNER/OPERATOR/AUDITOR/SYSTEM RBAC, idempotency fingerprints, duplicate directives and queue workers, freezable state, recovery primary+secondary incident linkage, event/audit log persistence and vault revisions.

**Property-based and metamorphic tests:** Derived invariants from DOC-C only (e.g. canonical key-order invariance, array-order non-invariance, reject non-JSON getters/cycles, idempotency exactly-once logical effects, revision monotonicity, deny unauthorized action under arbitrary valid inputs). Use pinned deterministic generator and recorded seeds ONLY in test harness if permitted; never introduce randomness into authoritative production decisions. A seeded test is not mathematically exhaustive.

**Mutation effectiveness:** For *high-risk algorithms only*, safely run bounded isolated mutations such as inverted comparator, off-by-one TTL, wrong role allowed, discarded transaction rollback, rejected/no-op event linkage, duplicate enqueue and timeout boundary; verify tests detect each mutation. Record mutant count/killed/survived/timeouts with exact mutation ID. Never mutate live Product/branch or leave altered source committed. Do not claim mutation coverage without actual runs.

**Model-based state checking:** Extract DOC-C FSM allowed events/transitions and guards, generate valid/invalid trace tests and replay deterministic state sequences; compare TypeScript vs Rust representations where both are authoritative. Invalid transition must not silently mutate state. Evidence must tie each reachable state transition and rejection class to tests.

**Fault injection:** Provider unavailable, malformed upstream response, partial outage, Redis disconnect, database transaction abort, queue worker crash/restart, source HEAD race, idempotency collision, ledger corruption, stale revision, replay, clock/TTL boundaries, bad signature, missing rollback. In each case assert fail-closed behavior, no leaked secrets or false successful outcome, durable recovery where required.

**Security:** Test actual HTTP boundary and permission checks with hostile inputs (oversize, Unicode, prototype pollution, request smuggling relevant to stack, unsafe headers, CSRF, injection, path traversal), and no public anonymous writes. Prefer benign sandbox tests; do not target external users or production services.

**Performance:** Measure before/after on identical hardware/runner/config and representative load; record latency quantiles, peak memory, throughput, DB query and queue lag where relevant. Performance improvement never excuses correctness regression; do not publish invented numbers.

**End-to-end:** Browser flows with real backend state and permissions; proof that button actions affect authorized real state and invalid state displays correct non-success UI. E2E must run, not a screenshot or static test title.

## 06. COMMAND DISCOVERY AND REAL EXECUTION

Read actual package.json, scripts, Cargo workspace files and CI definitions from CURRENT HEAD before choosing commands. Existing observed candidates to validate and RUN where applicable:
~~~
npm ci
npm run check:canon-source
npm run check:doc-c
npm run check:boundaries
npm run check:static-determinism
npm run check:six-system-spec
npm run typecheck
npm run lint
npm run test:contract
npm run test:integration
npm run test:all
npm run test:coverage
npm run check:coverage
npm run build:web
cargo test --locked --workspace --all-targets
git diff --check
~~~
Use node/npm and Rust toolchains matching actual repo. For DB/Redis/browser, use safe isolated services and recorded command environment. For any failure, record run SHA, runner identifier if real, log locator, failure category and next diagnostic. CI short-circuit with missing steps/logs is NOT automatically a code bug. If GitHub Actions is unavailable, run equivalent local proof if authorized, but maintain CI/Doc-E external gate BLOCKED. Do not forge signoff E11, rollback E12 or change release verifier to say passed.

## 07. HARD STOP AND ANTI-LOOP RULES

- P0 failure proven: prevent any release signoff and queue a prioritized fix. Noncritical ready work may continue under normal isolation.
- If identical action twice returns same failure with no new evidence, STOP brute-force retries; classify SOURCE / RUNNER / PERMISSION / NETWORK / SPEC_CONFLICT / STALE_HEAD. Change diagnostic method, choose independent ready work.
- If 2 attempts at a particular patch fail regression, freeze that patch, restore uncommitted sandbox state safely, investigate root cause and dependent contracts, do not ram through a third speculative change.
- If a test hangs or consumes excessive memory, terminate isolated job safely and record resource-limited verdict; lower parallelism, do not modify production thresholds just to pass.
- Missing original DOCX SHA or unresolved authority => freeze impacted spec-based mutations. Missing Product branch write permission => do not modify Product; still run authorized isolated tests and produce truthful handoff.
- Destructive production operations, new branch creation, secrets, billing, deployment, auth policy weakening, fake event proof, history rewrite or unverified operation are forbidden until explicitly approved where approval could lawfully apply.
- No guaranteed background work. On real tool/session limits, serialize full resumable checkpoint and stop truthfully.

## 08. MACHINE-CHECKABLE EVIDENCE AND ACCEPTANCE

Write journal records compatible with EXECUTION/20261011-NEXY-V8-ATOMIC-EVIDENCE-SCHEMA.json and explicit acceptance states. A claimed PASS for any atom needs:
- original exact spec_SHA256 and P locator;
- current frozen Product HEAD with source blob SHA, full source and dependency proof;
- actual positive + relevant negative execution, exact commands, toolchain, logs, exit code 0;
- full affected regression and post-edit GitHub readback; review evidence;
- no unresolved critical conflict or blocked required gate.
For a product release, additionally prove actual DOC-E E1–E12 and authorized signoffs, not copied historical report. Treat any missing required evidence as NOT_VERIFIED or BLOCKED, never PASS.

Maintain FOUR separate completion ratios (real numerators/denominators): file full-read coverage; file semantic coverage; in-scope atomic spec behavior verified; external release gates accepted. Excluded/deferred items do not inflate acceptance. Unknown denominator means NO PERCENTAGE, not 100%.

Per cycle report machine-usable:
~~~
RUN_ID (real) | SPEC_SHA | PRODUCT_HEAD_BEFORE -> AFTER
ATOM_ID + P_LOCATOR | source blob list and path
REPRODUCER RED_COMMAND, exit + log digest
FIX_DIFF + SHA | GREEN_COMMANDS, exits + log digests
TARGETED / INTEGRATION / SECURITY / MUTATION / BUILD verdicts
SIGNED? | E1-E12 status | commit/readback or PATCH_READY
FAILURES / BLOCKERS / NEXT_READY_ATOM
~~~
Do not assert that a file was read, a test was run, an AI agent collaborated, or a commit was written unless actual tool evidence proves it.

## 09. EXIT CONTRACT

**SUCCESS only when** every original in-scope atomic DOC-C requirement and supported DOC-D/storage/auth obligation has full current-HEAD behavior proof, all applicable unit/contract/integration/E2E/security and mutation obligations pass, no failing critical source or unresolved conflict, DOC-E E1–E12 are genuinely satisfied where required, release-signoff is authorized, and independent evidence readback passes. This is rigorous software acceptance rather than a mathematical guarantee of bug-free behavior.

**PARTIAL or BLOCKED** if any of the above is missing. Explain precise numerator/denominator, exact unresolved task IDs, blocker proof, last Product HEAD, all actual commits, and next exact executable actions; persist checkpoint into AI-CONTEXT for a new chat/Codex task. Do not pretend an idle prompt, saved policy or ChatGPT chat continues by itself.

**EXECUTE:** Using these maps and verified permission, start the highest-value READY reproducible defect or missing normative obligation, run real RED tests and fix it; then continue the next safe engineering task while this session can execute.
