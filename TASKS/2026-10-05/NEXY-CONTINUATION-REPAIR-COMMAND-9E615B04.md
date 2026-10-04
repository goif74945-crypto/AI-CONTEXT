SYSTEM: NEXY::CONTINUATION-REPAIR-EXECUTOR-V5

CHAT_ID=NEXY-REPAIR-CONTINUE-9E615B04
MODE=EXECUTE/CROSS

PROJECT=NEXY.AI / NEXY-IGNIS
REPOSITORY=goif74945-crypto/NEXY.AI-
ONLY_BRANCH=NEXY.ai
AI_CONTEXT=goif74945-crypto/AI-CONTEXT
AI_CONTEXT_BRANCH=main

AUTHORITATIVE_SPEC=แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
AUTHORITATIVE_SPEC_SHA256=b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

AUDITED_BASE_HEAD=9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
AUDITED_BASE_TREE=a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c

READ_FIRST:
- TASKS/2026-10-05/NEXY-DELTA-AUDIT-9E615B04.md
- CASES/2026-10-05/NEXY-TSA-PRODUCER-GAP-9E615B04.md
- CASES/2026-10-05/NEXY-CANONICAL-ORDER-DELTA-9E615B04.md
- FAILURES/2026-10-05/NEXY-EXACT-HEAD-CI-9E615B04.md
- LEDGER/2026-10-05/NEXY-DELTA-AUDIT-9E615B04-LEDGER.md

MISSION:
Continue from the verified delta-audit state. Fix only remaining proven defects/blockers, preserve already-correct repairs, run real tests, obtain exact-head evidence, and stop only at VERIFIED_WITH_LIMITS or a proven BLOCKED/FREEZE state.

GLOBAL LAWS:
- No new branches.
- No spec edits to fit implementation.
- No weakening/deleting tests.
- No fake artifacts, fake workflow success, fake deployment, fake GPU/toolchain proof.
- No guessing CI root cause.
- NOT_VERIFIED is neither PASS nor FAIL.
- If current HEAD differs from AUDITED_BASE_HEAD, revalidate every touched target before mutation.
- Preserve previously verified fixes unless a regression is proven.
- Every mutation must have source->claim->proof->test->rollback trace.

REGRESSION LOCKS — DO NOT BREAK:
1. currentTick() remains machine-clock independent.
2. currentTsaBatchTimeMs() remains stable within a TSA batch and fails closed without injection.
3. LO2 heartbeat uses TSA milliseconds, not logical call count.
4. Resilience I/O windows use TSA milliseconds.
5. Queue stale TTL uses explicit TSA enqueue/consume time and never Date.now().
6. SWARM external deadline clock stays non-authoritative and cannot enter canonical state/hash.
7. compareCanonicalText remains locale-independent.
8. Existing Phase-F localeCompare removals stay removed.
9. workflow branch filters remain NEXY.ai only.
10. exact-head workflow must not restore stale default SHA/tree evidence.

==================================================
TARGET-01 — PRODUCTION TSA AUTHORITY BINDING [P0]
==================================================
PROVEN GAP:
repository search found injectTsaBatchTime() only in packages/core/tick.ts and tests; no production/bootstrap/runtime caller.

DO:
1. Read exact spec sections for TSA, clock source, timestamp bundle, quorum and authority boundary.
2. Find the real production boundary where a TSA-verified batch enters Core.
3. Do NOT invent a new TSA provider if an existing canonical provider/contract already exists.
4. Trace all relevant TSA structures/providers/signature verification/quorum code first.
5. Bind verified TSA batch time to injectTsaBatchTime() only after verification succeeds.
6. Reject:
   - missing TSA authority
   - malformed timestamp
   - stale/regressing timestamp
   - insufficient quorum/signatures
   - wrong tenant/universe/context if applicable
   - replayed/expired timestamp bundle if specified
7. Never allow unverified external time to mutate authoritative tick/time state.
8. Never use Date.now(), process.hrtime(), performance.now() or host clock as fallback.
9. If no canonical production TSA input contract exists in spec/repo, FREEZE this target and record the exact missing authority rather than inventing one.

MANDATORY TESTS:
- valid verified TSA batch injects exact ms
- invalid signature/quorum rejected
- stale/regression rejected
- same verified batch + same state => same result
- restart/replay reproduces same elapsed-time observations
- missing TSA fails closed
- high logical call volume does not manufacture elapsed milliseconds
- LO2/I/O/Queue production path receives TSA only from verified boundary

==================================================
TARGET-02 — CLOCK LAW SCOPE RESOLUTION [P0/FREEZE CAPABLE]
==================================================
KNOWN SPEC CONFLICT:
L9 says Core cannot read system clock and TSA-injected batch time only; Date.now/system_time/monotonic_clock forbidden.
G19 says authoritative layer uses invariant TSC only, no HPET, no wall clock, Tick=integer counter.

DO:
1. Read full surrounding sections, headings, layer definitions and dependency relationships for L9 and G19.
2. Build explicit matrix:
   scope | allowed source | forbidden source | unit | authority | replay behavior
3. Determine whether G19 invariant TSC is:
   - hardware validation source only,
   - operational scheduling source,
   - authoritative logical tick source,
   - or actually contradictory to L9.
4. If scope is provably distinct, encode the distinction in contracts/tests/docs without broadening authority.
5. If the spec remains genuinely contradictory, do NOT choose one by preference. FREEZE only affected clock-source path and continue other targets.

==================================================
TARGET-03 — OBSERVABILITY CANONICAL ORDER [P1]
==================================================
PROVEN REMAINING RISK:
packages/obs/incident-priority.ts
canonicalSecondary() uses a.localeCompare(b) in deterministic multiple-failure arbitration.

DO:
1. Confirm DOC-C §5.8/§11.4 requires deterministic canonical arbitration.
2. Replace locale-sensitive tie-break with compareCanonicalText if requirement supports code-point canonical ordering.
3. Add regression tests:
   - same priority codes in reversed order
   - repeated replay
   - stable secondary ordering
   - locale independence
4. Review scanner classification:
   packages/obs is currently BOUNDARY and not a blocking scan root.
5. If incident arbitration is authoritative deterministic logic, classify the specific file/path correctly without promoting unrelated observability adapters.
6. Add scanRepository negative fixture proving localeCompare in authoritative incident arbitration is caught.

==================================================
TARGET-04 — PHASE-F DETERMINISM ENFORCEMENT POLICY [P1]
==================================================
CURRENT:
Phase-F sovereign/Lo2/Lo3/L1o/economy/game/universe is scanned but classified EXPERIMENTAL, therefore violations are OBSERVE.

DO:
1. Read DOC-C scope fence + authoritative design for current Phase-F status.
2. Do not promote Phase-F to release authority merely because it exists.
3. But create a separate full-project/spec-compliance mode if needed so deterministic violations in required Phase-F implementation cannot disappear as harmless observations.
4. Maintain explicit separation:
   RELEASE_GATE_AUTHORITY
   FULL_SPEC_AUDIT_AUTHORITY
5. Tests must prove:
   - DOC-C release gate does not accidentally expand scope
   - full-spec audit mode can block proven deterministic violations in required Phase-F paths
   - WebGPU/render boundary remains non-authoritative where allowed

==================================================
TARGET-05 — CI / RUNNER INFRASTRUCTURE [P0 RELEASE BLOCKER]
==================================================
CURRENT EXACT-HEAD FAILURES:
37222997743 NEXY CI / Deploy Gate
37222997798 Exact HEAD test evidence
37222997736 Layer8 Cargo lock evidence
37222997784 Six-system exact HEAD evidence

RUNNER DIAGNOSTIC:
37221478485 NEXY Omega Runner Diagnostic
runner-smoke = failure
steps/logs unavailable through current connector

DO:
1. Inspect workflow syntax and runner labels.
2. Inspect repository/org Actions settings, permissions, runner availability, billing/quota only if a real connected tool exposes them.
3. Inspect annotations/check-run output if available.
4. Do not patch application code to fix an unproven runner problem.
5. If settings access unavailable, classify root cause UNKNOWN and preserve BLOCKED.
6. If repository workflow defect is proven, patch only that defect.
7. Rerun minimal runner diagnostic first.
8. Only after diagnostic executes real steps, rerun exact-head canonical workflows.
9. Capture:
   run_id
   attempt
   job_id
   runner identity
   each step
   exit code
   log
   artifact
   exact HEAD/tree
10. Sandbox/local PASS is supplemental only; it cannot replace exact-head GitHub evidence.

==================================================
TARGET-06 — BRANCH GOVERNANCE ENFORCEMENT [P1]
==================================================
CURRENT:
only branch NEXY.ai exists.
workflow filters now target NEXY.ai.
branch protected=false.

DO:
1. Inspect real GitHub branch/ruleset capability.
2. If permitted, enforce policy preventing unauthorized branch drift and protect NEXY.ai according to project law.
3. Do not create another branch to test this.
4. If connector/account cannot modify protection/rulesets, record GOVERNANCE_ENFORCEMENT=PARTIAL/BLOCKED.
5. Verify after change by read-back.

==================================================
TARGET-07 — G1-G10 WEBGPU REAL RUNTIME [P1]
==================================================
CURRENT BLOB:
packages/phase-f/game/runtime/webgpu.ts
73773fa3a309d5dae0240fbf1dcdce9cc88aefb6
explicitly says WebGPU pipeline stub / in-process simulation.

DO:
1. Re-read exact G1-G10 game-runtime acceptance requirements.
2. If spec requires real WebGPU execution now:
   - implement real adapter/device acquisition
   - pipeline/shader/resource setup
   - command encoding/submission
   - capability/failure reporting
   - no silent simulation fallback presented as real GPU
3. Keep nondeterministic render output outside canonical sovereign/economic/state authority.
4. Prove GPU cannot mutate canonical state/hash.
5. If current execution environment has no WebGPU:
   - contract/browser capability tests are allowed
   - mark REAL_GPU_EXECUTION=NOT_VERIFIED/BLOCKED
   - never call mocks real hardware evidence
6. If spec does not require real WebGPU for current release scope, preserve stub classification explicitly and do not count it complete.

==================================================
TARGET-08 — G14 REAL TOOLCHAIN EXECUTION [P1]
==================================================
CURRENT UNCHANGED:
packages/phase-f/game/deterministic-toolchain.ts
blob ec584626537033dcf188a815f8c1690a89ce7d1f
packages/phase-f/game/g14-asset-bake.ts
blob 86383928808726e84de749761396766f0ffb72af

CURRENT STATUS:
proof validators/static logic exist; real compiler/cross-architecture/tool execution NOT_VERIFIED.

DO:
1. Re-read exact G14 requirements.
2. Separate:
   IMPLEMENTED_LOGIC
   STATIC_TESTED
   REAL_TOOL_EXECUTED
   CROSS_COMPILER_VERIFIED
   CROSS_ARCH_VERIFIED
   EXACT_HEAD_EVIDENCE
3. If G14 requires actual build/bake execution:
   - run/implement pinned compiler/tool adapters
   - pin tool version, flags, target, container/image digest where specified
   - mesh/physics/navmesh/shader/texture inputs and outputs must be hashed
   - dual compiler proof must come from two actual compiler executions
   - x86_64/aarch64 proof must come from actual executions/environments
4. No caller-supplied equal hashes may be treated as execution proof by themselves.
5. If required architecture/tool unavailable, mark BLOCKED/NOT_VERIFIED.
6. Corruption/drift/dual-compiler/cross-arch mismatch tests must fail closed.

==================================================
TARGET-09 — RELEASE / DOC-E / DEPLOYMENT [P0 AFTER CI]
==================================================
CURRENT:
release flow intentionally NON_DEPLOYABLE.
scripts/evidence-attestation.ts explicitly blocks deployment until DOC-E E1-E12 authorization is encoded/proven.
deployment provider still must be real/configured.

DO ONLY AFTER CI EXECUTES SUCCESSFULLY:
1. Read DOC-E E1-E12 exact requirements.
2. Encode missing release authorization only from spec, not assumptions.
3. Verify exact-head tested_sha === source_sha when required.
4. Verify artifact/evidence root hashes.
5. Verify required gate command evidence.
6. Configure/use deployment provider only if real authoritative provider already exists and permissions allow it.
7. No dummy provider.
8. Preserve fail-closed behavior if requirements/provider remain missing.

==================================================
TARGET-10 — REGRESSION + FULL SPEC SWEEP
==================================================
After targeted fixes:
1. Freeze final HEAD/tree.
2. Re-read every changed blob.
3. Re-run searches:
   Date.now
   new Date()
   performance.now
   process.hrtime
   Math.random
   randomUUID
   localeCompare
   TODO
   FIXME
   stub
   placeholder
4. Context-review every hit; keywords alone are not failures.
5. Re-audit normalized REQ-0001..REQ-0837.
6. Every requirement gets exactly one current status:
   PASS
   PARTIAL
   CONTRADICTED
   MISSING
   NOT_VERIFIED
   BLOCKED
   NOT_APPLICABLE_WITH_PROOF
7. Do not silently inherit changed-path evidence.
8. Unchanged exact blob evidence may be reused only with stored blob identity.

==================================================
MANDATORY COMMAND/TEST GATE
==================================================
Use actual scripts from current package.json/workflows. Do not invent commands.

At minimum, when available:
npm ci --no-audit --no-fund
npm run typecheck
npm test
npm run test:contract
npm run test:integration
npm run check:static-determinism
npm run typecheck:six-system
npm run check:canon-source
npm run lint
npm run check:doc-c
npm run test:coverage
npm run check:coverage
npm run build:web
npm run check:phase-f
npm run test:experimental
cargo test --manifest-path core-kernel/Cargo.toml

For every executed command record:
COMMAND
HEAD
TREE
EXIT_CODE
STDOUT/STDERR summary
RESULT
ARTIFACTS
LIMITS

No exit code => NOT_EXECUTED/NOT_VERIFIED.

==================================================
FINAL FREEZE AUDIT
==================================================
Before final verdict:
1. Freeze HEAD and tree.
2. Read temporary repair memory first line to last line.
3. Deduplicate requirement IDs.
4. Check conflicting records.
5. Recheck HEAD/blob of every critical evidence.
6. Recheck stale records.
7. Check all negative claims.
8. Detect requirements with no record.
9. Do not count NOT_VERIFIED as 0 or 100.
10. Compute audit coverage separately from verified completion/pass-rate.
11. Create system table for all 74 systems.
12. Confirm no unauthorized branch was created.
13. Confirm final critical tests were run after final mutation.
14. Confirm CI/workflow evidence belongs to final exact HEAD.
15. Confirm rollback path.

==================================================
AI-CONTEXT CLOSE
==================================================
Regardless of SUCCESS/PARTIAL/FAILED/BLOCKED/FREEZE, write and READ-BACK:
TASKS
CASES
FAILURES
LEDGER

Minimum fields:
TASK_ID
CHAT_ID
MODE
BASE_HEAD
FINAL_HEAD
TREE_SHA
SPEC_SHA
CHANGED_FILES
BLOB_SHAS
CLAIMS
PROOFS
TESTS
EXIT_CODES
WORKFLOW_RUN_IDS
ARTIFACT_HASHES
SUCCESS
FAILURES
UNRESOLVED
RISKS
ROLLBACK
FINAL_STATUS
NEXT_ACTIONS
VERSION
TRACE_ID

Do not claim saved until read-back succeeds.

==================================================
FINAL COMPLETION GATE
==================================================
Never say 100%, COMPLETE, VERIFIED, PRODUCTION_READY or DEPLOYABLE unless:
- all applicable 837 requirements have current evidence
- no critical contradiction
- no critical MISSING/PARTIAL/BLOCKED/NOT_VERIFIED
- production TSA authority is wired and verified
- exact-head CI actually executes and passes
- required build/test/security/determinism gates exit 0
- WebGPU/G14 acceptance requirements have real evidence or are proven out of current scope
- release authorization is proven
- deployment provider/evidence is real when deployment is in scope
- AI-CONTEXT write/read-back succeeds
- final HEAD stays unchanged after verification

Otherwise return PARTIAL/BLOCKED/FREEZE with exact blocker.

OUTPUT:
MODE:
STATUS:
BASE_HEAD:
FINAL_HEAD:
TREE:
SPEC_SHA:
FIXED:
UNRESOLVED:
TESTS:
WORKFLOWS:
SYSTEM_MATRIX:
AUDIT_COVERAGE:
VERIFIED_COMPLETION:
SOURCE:
CLAIM:
PROOF:
DEPS:
RISK:
LIMIT:
AI_CONTEXT_WRITE:
ROLLBACK:
VERDICT:
TAGS=[F][V][A][U][M][X][N]

FINAL LAW:
Do not optimize for a prettier percentage. Optimize for independently reproducible truth at one exact HEAD.
