# NEXY — Codex Next Execution Command 004

SYSTEM: NEXY::SPEC-UNBLOCK-TIME-BOUNDARY-SANDBOX-CLOSURE-V1
MODEL TARGET: Codex / GPT-5.6-class engineering executor

MODE:
EXECUTE_NOW
ENGINEERING
EVIDENCE_DRIVEN
FAIL_CLOSED
NO_GUESS
NO_FAKE_PASS
CURRENT_HEAD_AWARE
MULTI_CHAT_SAFE
CONTINUOUS_CLOSURE

## 0. CONTINUE FROM VERIFIED CURRENT STATE

Last reported product HEAD:
8b406a63f10aa1424225a80453393af2e4cb78b5

Last reported AI-CONTEXT HEAD:
2e27e349e8dd3f6ae3c250588f11d8d31b9fd8da

Last matrix:
98 total
14 CURRENT_VERIFIED
9 CURRENT_PARTIAL
4 CURRENT_MISMATCH
62 CURRENT_NOT_VERIFIED
4 SPEC_SOURCE_ACCESS_BLOCKED
5 INFRA_BLOCKED
39/98 substantively reviewed

Do not repeat the report and stop.

Re-query both HEADs immediately. If product HEAD changed, inspect intervening commits before any mutation.

## 1. SPEC SOURCE IS NOW AVAILABLE AND HASH-VERIFIED

A fresh audit of the actual uploaded authoritative DOCX produced:

FILE:
แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx

SHA-256:
b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

REQUIRED SHA MATCH:
YES

Use AI-CONTEXT evidence:
EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md

The evidence record contains exact paragraph locators from the hash-matching DOCX.

Therefore do NOT retain SPEC_SOURCE_ACCESS_BLOCKED merely because your own workspace does not contain the binary DOCX. You now have a hash-verified source extraction with explicit locators. If a row needs content not present in that extraction, block only that row and request/add the missing locator rather than restoring a global spec block.

## 2. AUTHORITY RULING — MUST APPLY

DOCX P9837–P9845 states:
- DOC-A = vision canon
- DOC-B = system law
- DOC-C = build spec
- DOC-D = product design pack
- DOC-E = deployment evidence pack
- build obligation comes from DOC-C only
- deploy approval comes from DOC-E only

Consequences:

AUTH-01:
Reclassify from SPEC_SOURCE_ACCESS_BLOCKED after recording the verified SHA match.

AUTH-02:
Re-audit against the authority split above. If current architecture honors it, reclassify with current proof.

AUTH-03:
Early prose says OTAC TTL 10–15m / session 1–6h.
Final DOC-C P9910–P9938 defines:
- otac_ttl_ms = 300000
- otac_max_attempts = 5
- otac_lock_window_ms = 900000
- session_ttl_ms = 21600000
- concurrent_sessions_per_user = 5

Because DOC-C is the sole build authority, do NOT change current code to satisfy the older prose if current source matches DOC-C. Preserve the older prose as a historical authority conflict note. If current source/tests prove the DOC-C values, AUTH-03 is authority-resolved rather than a live product mismatch.

SCOPE-01:
Use DOCX P9644–P9689 Section 17. Re-audit current repository scope against:
IN: deterministic directive execution, multi-agent pipeline, consensus/release policy, vault revisioning, auth/session/OTAC, observability/incidents, RBAC/UI truth layer.
OUT: voice orchestration, blockchain, real-time 3D UI, public anonymous writes, AR/VR/XR, IoT control, quantum-safe layer for vNEXT, holographic UI.
DEFERRED: advanced policy simulation dashboard, multi-tenant org hierarchy, fine-grained per-project config policy, provider marketplace.

Do not mass-promote. Record exact current source/config proof.

## 3. NEXT ROOT-CAUSE TARGET: DIRECTIVE SUBMISSION / TSA BOUNDARY

Observed final-head behavior:
- browser: 9 pass / 2 fail
- failing flows: OWNER directive submission / canonical pipeline run detail
- persisted dispatch failure: TSA_TIME_AUTHORITY_UNAVAILABLE
- PIPE-07 and QUEUE-06 classified INFRA_BLOCKED

Current source observations at 8b406a63:
- packages/queue/dispatch.ts requires currentTsaBatchTimeMs() before enqueue.
- packages/core/tick.ts exports injectTsaBatchTime().
- current code search found injectTsaBatchTime() production definition, but callers were found only in tests; no current production caller was found.
- broader sovereign code contains 3-TSA / 2-of-3 verification logic, but final DOC-C build spec does not itself state a TSA requirement for POST /api/directives or queue enqueue.

This creates a critical authority/integration question.

### Required proof before mutation

A. Re-run repository-wide current-head search for:
- injectTsaBatchTime
- currentTsaBatchTimeMs
- evaluateAuthorityTime
- tsaQuorum
- queue submission/bootstrap time initialization

B. Build a source-level call graph from external/bootstrap time input to queue dispatch.

C. Determine which of these is true:

CASE 1 — production verified-time bridge exists:
Then diagnose why it is not activated in browser/runtime and repair that exact integration path.

CASE 2 — no production bridge exists, but an explicit DOC-C/DOC-B obligation requires verified TSA for vNEXT queue dispatch:
Then implement the smallest trusted boundary that converts already-verified authoritative time evidence into the Core tick boundary. It must use existing verification law rather than accepting raw arbitrary timestamps.

CASE 3 — no production bridge exists and TSA hard-dependency came from broader non-DOC-C sovereign/experimental architecture without a final vNEXT build obligation:
Then treat the queue hard-dependency itself as a scope/implementation defect. Remove or isolate the unauthorized dependency in a way that still preserves DOC-C queue TTL/idempotency semantics. Do not import experimental sovereign architecture into canonical vNEXT merely to make tests pass.

If authority remains genuinely unresolved after the hash-verified DOCX evidence, freeze only this path and continue other READY work.

## 4. ABSOLUTE TIME-SAFETY RULES

FORBIDDEN:
- Date.now() as authoritative Core time
- new Date() as authoritative Core time
- performance.now() / hrtime as authoritative Core time
- arbitrary environment timestamp promoted to TSA
- hardcoded timestamp in production
- fake TSA signature
- verifier that always returns true in production
- bypassing 2-of-3 when that authority path is applicable
- weakening fail-closed behavior solely to make browser green

Test fixtures may be deterministic and use test verifiers ONLY when the test still exercises the real verification boundary and cannot leak into production configuration.

The broader DOCX time policy records 3 TSA / >=2 valid signatures, anomaly on excessive TSA/chain delta, and 24h degraded freeze. Do not invent a different quorum law.

IMPORTANT:
The broader time policy is not automatically a DOC-C vNEXT build obligation. Prove the authority dependency before coupling canonical queue code to it.

## 5. TSA REGRESSION / BROWSER PROOF

If a code defect is confirmed and repaired:

Add targeted tests proving all applicable cases:
- no authoritative time evidence => fail closed where required
- invalid/insufficient TSA evidence => rejected
- duplicate/unknown witnesses => rejected when using TSA quorum path
- excessive TSA/chain delta => rejected/anomaly
- valid current evidence => batch time becomes available only through the trusted boundary
- stale/regressive authoritative batch => rejected
- browser directive submission succeeds only when the legitimate required boundary is satisfied
- no production route can invoke the test-only reset/injection bypass

Then rerun the two previously failing browser tests first, followed by applicable integration/contract/full gates.

Do not claim UI defect closure merely because the 503 disappeared; prove the queue/run state is semantically correct and read-back succeeds.

## 6. SECOND ROOT-CAUSE TARGET: LO3 BWRAP RUNTIME ROOT

Current experimental result:
781 pass / 10 fail in tests/integration/lo3-cage-command.spec.ts.

Current source proof:
packages/phase-f/lo3/cage.ts selects bwrap when available and binds read-only:
- /usr
- /lib
- /lib64
- /etc/ssl
plus proc/dev/tmpfs.

The tested command is process.execPath.
On the failing runner, Node was under /opt and therefore outside the bound runtime roots.

This is a plausible current source/runner mismatch. Confirm it on the current runner before patching.

### Sandbox authority from the verified DOCX

P4137–P4149 requires isolation via container sandbox, namespace isolation, syscall filter, memory isolation, optional WASM.
P4886–P4927 requires recursive sandbox capability shrink and forbids a sandbox app from mounting external FS or spawning privileged containers; actions go through parent mediation.

The spec does NOT authorize simply disabling bwrap to make tests pass.

### If the /opt runtime-root cause is confirmed

Repair the Linux bwrap command builder minimally so the trusted executable/runtime needed to launch the child is available read-only without creating a guest-controlled arbitrary host mount primitive.

Required properties:
- resolve/validate trusted command path before constructing mounts
- never accept arbitrary mount source from untrusted model/user input
- expose the minimum read-only runtime root needed for that trusted executable
- preserve unshare/isolation behavior
- preserve network policy
- preserve cgroup/resource controls
- do not bind the whole host filesystem
- do not make /opt globally writable
- do not fall back to dev-naive merely because the stronger backend exposes a path-layout bug

Add negative tests for path traversal/untrusted runtime-root injection and a positive regression for an executable located outside /usr (e.g. a controlled temporary/test fixture or environment-appropriate trusted path).

Then rerun the 10 previously failing tests and the whole experimental suite.

If current runner no longer reproduces /opt failure, do not mutate from historical logs alone.

## 7. CI ZERO-STEP FAILURES

Current-head GitHub workflow runs failed before executable steps.

Keep GATE-03/04/05 as INFRA_BLOCKED unless new evidence identifies the actual current cause.

Do NOT:
- label them code failures without steps/log evidence
- weaken workflows
- delete required jobs
- add continue-on-error
- fabricate a CI pass from local results

Local runner PASS is useful behavior evidence but does not equal release/deploy gate PASS.

## 8. DOC-E RELEASE GATE — DO NOT FAKE

Verified DOCX P10917–P10999 requires real evidence artifacts and signoffs.

No deploy without:
- engineering signoff
- security signoff
- migration signoff
- rollback verification
- monitoring verification

Also required include queue-worker readiness, alarm verification, incident drill, deploy runbook, release signoff record, rollback playbook execution proof.

Therefore GATE-06 / EVID-04 / EXP-06 and deploy readiness MUST remain NOT_VERIFIED unless real artifacts exist.

Do not generate fake human signoffs.
Do not convert isolated DB migration rollback into full application rollback proof.

## 9. HISTORICAL EVIDENCE HYGIENE

AUTH-11 and EVID-01/02/03 currently remain mismatches because historical evidence binds old heads/hashes.

Preserve historical payloads.
Do not rewrite them to appear current.

Create fresh current-head evidence as superseding records only after the underlying command/test actually ran.

If an obsolete file has a misleading name such as current-head-attestation.json, do not delete history just to improve matrix score. Explicitly mark/supersede it through current evidence and fix consumers so they cannot treat it as current.

## 10. REVIEW THE 62 CURRENT_NOT_VERIFIED ROWS WITHOUT MASS PROMOTION

After the two root-cause workstreams above, continue substantive audit in bounded slices.

Priority slices:
1. CON-01..06 + VAL-01..03
2. FSM-01..04 + PIPE-01..06
3. API-01..07 + AUTH-05..09
4. STORE-01..05
5. RBAC-01..03 + OBS-01..04
6. QUEUE-01..05
7. UI-01..05
8. SCOPE-03
9. EXP-01..04

For each row:
- read exact authoritative locator
- read current source/tests
- bind immutable source hashes/HEAD
- execute tests when behavior proof is required
- classify independently

A passing full suite is NOT enough to mass-promote unrelated rows.

## 11. CONCURRENCY / WRITE FENCE

Before every product write:
- re-read NEXY.ai HEAD
- compare expected vs actual HEAD
- inspect intervening commits
- recompute patch if target files changed
- never force-push
- never create/delete/rename branches
- never overwrite unseen work

Prefer minimal atomic commits by root cause.

## 12. FINAL-HEAD VALIDATION

After each repair group:
- targeted regression
- relevant contract/integration suite
- typecheck
- static/boundary/determinism checks as applicable

Before any project-level final claim:
1. freeze one final product HEAD
2. rerun all required applicable gates against that exact HEAD
3. no post-validation code/test/config mutation
4. bind logs/evidence to that same HEAD
5. preserve CI vs local distinction
6. apply DOC-E release requirements separately

Any later mutation invalidates final-head proof and requires rerun.

## 13. AI-CONTEXT WRITEBACK

Write sanitized current records to AI-CONTEXT/main:
TASKS/
EVIDENCE/
LEDGER/
FAILURES/ when applicable
CASES/ for integrity/authority incidents

Include:
- start/end product HEAD
- start/end AI-CONTEXT HEAD
- spec source record used
- rows reclassified
- files changed
- commits
- tests authored/executed
- exact results
- browser/experimental rerun outcomes
- CI state
- unresolved blockers
- rollback path
- next READY action

Read every write back.

## 14. PROHIBITED SHORTCUTS

No fake PASS.
No placeholder.
No test deletion.
No weakened assertions.
No skip/only to hide failure.
No required continue-on-error.
No threshold reduction.
No source/spec rewrite to fit implementation.
No stale evidence promotion.
No arbitrary TSA injection.
No sandbox isolation downgrade.
No arbitrary host filesystem bind.
No mass row promotion from a single passing suite.
No human signoff fabrication.

## 15. MANDATORY PROGRESS RULE

In this same execution run, do not stop after planning.

At minimum perform:
A. spec-blocker reclassification using the verified authority record, AND
B. current-head proof of the TSA call-path case (1/2/3 above), AND
C. one concrete safe repair if a source-proven defect is confirmed.

If TSA path is authority-blocked, continue to the bwrap workstream or substantive row audit instead of globally stopping.

## 16. OUTPUT FORMAT

MODE:
STATUS:
TARGET_BRANCH:
START_HEAD:
END_HEAD:
AI_CONTEXT_HEAD:
SPEC_SHA256_STATUS:
SPEC_AUTHORITY_RECORD:
MATRIX_TOTAL:
CURRENT_VERIFIED:
CURRENT_PARTIAL:
CURRENT_MISMATCH:
CURRENT_NOT_VERIFIED:
SPEC_SOURCE_ACCESS_BLOCKED:
INFRA_BLOCKED:
SUBSTANTIVE_REVIEW_COVERAGE:
COMPLETION:
ROWS_RECLASSIFIED:
TSA_CALL_GRAPH_RESULT:
TSA_AUTHORITY_CASE:
TSA_REPAIR:
BROWSER_RERUN:
BWRAP_ROOT_CAUSE:
BWRAP_REPAIR:
EXPERIMENTAL_RERUN:
CI_STATUS:
CHANGED_FILES:
COMMITS:
TESTS_EXECUTED:
EVIDENCE_WRITTEN:
LOCAL_BLOCKERS:
NEXT_READY_ACTION:
VERDICT:

Allowed STATUS:
WORKING
PARTIAL
BLOCKED_LOCAL
FAILED
VERIFIED_WITH_LIMITS
PASS_100

## 17. BEGIN NOW

Re-query live HEADs.
Read EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md.
Reclassify the four SPEC_SOURCE_ACCESS_BLOCKED rows from current evidence where justified.
Then trace the production TSA call graph end-to-end.
Do not inject synthetic time.
If a real implementation/scope defect is proven, repair it and rerun the two browser failures.
Then inspect/repair the bwrap runtime-root defect only if current-run evidence confirms it.
Continue substantive row audit instead of stopping at remaining infrastructure-only blockers.