# NEXY::CODEX-SPEC-MAPPED-CONTINUOUS-ENGINEERING-V6 — EXECUTE_NOW

**FOR:** Codex engineering agent operating on `goif74945-crypto/NEXY.AI-`
**INTENT:** Audit original authoritative spec against every in-scope source file; discover genuinely missing or broken behavior; implement exactly-required code; execute real tests and repair regressions; continue successive useful engineering cycles in an **active session**, publish resumable proof.
**MODE:** `EXECUTE_NOW / PRODUCT_BUILDER / SPEC_EXACT / MAP_ACCELERATED / SINGLE_WRITER / RED_GREEN / SECURITY_FIRST / NO_FAKE_PASS / CONCURRENCY_SAFE / EVIDENCE_APPEND_ONLY / FAIL_CLOSED`
**NOT AN ACCEPTANCE CERTIFICATE:** This command cannot itself prove anything passed or make a paused runner execute forever.

## 00. FIRST ACTION: READ CONTROL MAP AND BRANCH GOVERNANCE

Obtain connected authorized repository access and read these **real files** at live AI-CONTEXT/main before deciding any edit:
1. `START-HERE-NEXY-IGNIS-CODEX-20261010.md`
2. `POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md`
3. `NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.md`
4. `NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.tsv`
5. `NAVIGATION/20261010-NEXY-AI-FROZEN-HEAD-889-BLOB-MANIFEST.tsv`
6. `COMMANDS/20261010-NEXY-CODEX-SPEC-EXACT-LONG-RUN-ENGINEERING-V5.md` (base engineering instructions; V6 adds and clarifies map and continuation)
7. `COMMANDS/20261009-NEXY-GPT6-SOL-143-ACCEPTANCE-REGISTER-V4.md` (**historical discovery**, not acceptance proof)
8. `EVIDENCE/20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT-INTERIM-GATE-REPORT.md` and `EVIDENCE/20261010-NEXY-CI-RUNNER-RELEASE-BLOCKER-DIAGNOSIS.md` (**leads to reproduce**, not current PASS).
9. Product `AGENTS.md` **from actual live product HEAD**.

Do not edit the Product merely from the historical report or presumed HEAD. The live baseline at this command's creation was:
`goif74945-crypto/NEXY.AI-` branch `NEXY.ai`, HEAD `58b1200bd61b867e917057d0019eea78ea9f6b2a`.
AI-CONTEXT/main may advance from peer writes: **refresh live HEAD**, never rely on this snapshot as current.

Start doing read/check/test/repair in this session, not only writing more prompts and stopping.

## 01. AUTHORITY AND SCOPE FREEZE

Authoritative byte-identical original: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`, SHA-256:
`b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.

- Locate the original DOCX through authorized attachments/user workspace; SHA256 hash **the actual bytes**. P anchors in map are **1-based DOCX paragraph numbers including empty paragraphs**; do not interpret P as page number.
- Read the original, and not merely the extracted map. Map is an index; it neither replaces normative full text nor claims every atomic requirement is indexed.
- DOCX `P09837–P09845`: DOC-A vision; DOC-B system law; **DOC-C build obligation**; DOC-D product design only where supported by DOC-C; DOC-E deployment proof/release signoff.
- **DOC-C P09886–P10499**: included/excluded, defaults, contracts, 12 canonical API handlers with their auth/RBAC/idempotency/retries/audit/error matrices, FSM, freeze/owner, incident linkage.
- **DOC-D P10500–P10722**: 12 screens, 14 named components, tables/forms/validation/permissions/mobile/empty/loading/trust. Check applicability with DOC-C.
- **Storage supplement P10723–P10835; auth hardening P10836–P10916**: inspect dependencies and implement supported build obligations; do not silently promote standalone aspirational clauses.
- **DOC-E P10917–P10999**: E1–E12 require real anchored run artifacts, not existence or simulated pass.
- Scope fence `P09644–P09689` and exclusions `P09900–P09909`: no voice/AR/VR/blockchain/IoT/quantum-safe/self-patch/anonymous write by stealth. Experimental `packages/phase-f` needs explicit scope classification, never included in vNEXT acceptance by default.

If original DOCX hash differs, **FREEZE affected spec-based implementation** and investigate; continue safe source inventory/diagnostics separately, no speculation.

## 02. SNAPSHOT-BOUND INVENTORY WITHOUT REPEATING THE UNIVERSE

The prebuilt atlas has 88 **navigation groups** and source Git manifest has 889 **tracked blobs** for frozen HEAD. These counts are not a requirement denominator or review status.

1. Run `git rev-parse HEAD`, `git status --porcelain`, `git ls-files -z`; fetch remote HEAD and recursively enumerated Git tree at exact revision.
2. If HEAD equals the atlas/manifest revision, validate hash/size/path and use atlas candidates directly to reach the relevant source and test. No need to repeatedly conduct unfocused full repo discovery.
3. If HEAD differs, compute `git diff --name-status <ATLAS_SHA>..<CURRENT_SHA>` (or authenticated API comparison); reconcile path moved/deleted/new, and rehash changed blobs; **retain still-correct unchanged locator mappings**. Never count a missing candidate filename as proof that a feature is absent.
4. Keep full manifest with per-path classification: `READ_FULL / BINARY_CLASSIFIED / GENERATED_IDENTIFIED / NOT_READ / ERROR`; classify every tracked file, including docs, workflows, Rust, TS, SQL, lockfiles and assets. A filename scan/search result is not a semantic review.
5. For each spec row, inspect the full implementation and its imports, callers, auth guards, database transactions, worker dispatch, downstream effects, test fixture fidelity, secrets/trust boundaries and logs. Mark independently `SOURCE_LOCATED`, `IMPLEMENTED_STATIC`, `TESTED_RUNTIME`, `BEHAVIOR_VERIFIED`, `FAILED`, `BLOCKED` or `OUT_OF_SCOPE`. No blanket status.
6. Generate **atomic** DOC-C acceptance records with stable IDs and exact original P text/location. Reconcile with 143 historical checkpoints and 88 navigation groups; do not stop at either number or compute fake 100% denominator.

## 03. EXPLICIT HIGH-VALUE PRIORITIES; VERIFY, DO NOT ASSUME

Existing AI-CONTEXT reports on `58b1200...` indicate candidate work:
- EX018 independent auth OTAC helper suite: 14 tested, 11 green, 3 red. Retrieve actual red inputs/logs; reproduce on fresh HEAD, ensure user-visible auth contract and fail-closed handling before smallest repair. Prior report is **candidate**, not independent reproduction in your session.
- CI on that HEAD: 4 workflows failed, including `NEXY CI / Deploy Gate` run `37899764374`; child jobs short-circuited and job logs returned BlobNotFound in prior access. Investigate runner assignment, account quotas/permissions and direct local tests separately; runner errors ≠ verified product bugs.
- The historical code may intentionally produce non-release-eligible attestation; do not weaken the verifier, forge E11 signoff or flip `NON_DEPLOYABLE` to pass green.
- Spec risky zones: canonical serialization and all hash consumers; OTAC replay/lock; session/device binding; idempotent concurrent directives and worker enqueue; stale processing/cancel; authority-guarded FREEZE/RECOVER; event/audit/secondary incident linkage; migration rollback and storage; UI permission truth and API response envelopes.
- Use `NAVIGATION/...` entries for precise source and spec anchor; do not uncritically trust named tests because they exist.

Select a `READY` task using **severity × evidence × scope relevance × dependency order**. Work on actual code when a reproducible gap is found; don't endlessly analyze already-complete source. If particular task blocked, advance another independent READY task.

## 04. ACTUAL ENGINEERING LOOP; REPEAT WHILE ACTIVE

For each atomic requirement:
- **DISCOVER:** read original clause and neighboring context; verify applicability and exact current functions/paths.
- **EVALUATE:** `IMPLEMENTED_AND_BEHAVIOR_PROVEN` => no edit, preserve code; `MISSING_OR_DEFECT_PROVEN` => implement; `CONFLICT/UNKNOWN` => freeze that edit and collect more evidence.
- **RED:** create/execute one or more test cases that fail before fix where possible; include hostile input, invalid auth, concurrency, non-determinism, drift, oversize, rollback, partial provider outage, error serialization, UI/backend mismatch.
- **CHANGE:** smallest complete production fix with no TODO/placeholder/mock production behavior and no feature not in spec. Prefer existing interfaces, no stealth breaking change.
- **GREEN:** rerun red tests, neighboring contract/integration suites, DB mocks and real DB/Redis when needed. Record command, cwd, runner environment, exit, exact tree hash, stdout/stderr artifact digest.
- **REVIEW:** threat and concurrency review, negative matrix, static/typing checks, full diff, untracked changes, generated artifacts, lockfile consistency, provenance.
- **COMMIT:** only with confirmed permissions and product policy, on **existing NEXY.ai branch only**; refresh HEAD immediately pre-write, use expected-head/CAS or equivalent, readback blobs and remote HEAD post-write. No creation of branch, hidden branch, fork, rebase/force-push, overwriting peer work. If mandatory test infrastructure blocked, keep honestly blocked/NOT_DEPLOYABLE; code can only be committed if applicable source-change acceptance gates are satisfied by real permitted evidence, not waived.
- **JOURNAL:** append a unique, sanitized exact-HEAD evidence record to `AI-CONTEXT/main/EVIDENCE`. Carry forward ledger, NOT pass-claims.
- **NEXT:** choose next READY task, proceed in same active session without soliciting confirmation for routine permitted changes.

Product source should receive **substantive updates as long as real, authorized, source-justified defects/requirements remain**, not an endless stream of empty commits. No agent can guarantee time-unbounded execution merely from this prompt. A scheduled future runner must be separately created and confirmed.

## 05. REAL EXECUTABLE VALIDATION (select commands only after verifying actual package/tool versions)

Execute in a **checked-out exact HEAD** and record logs/exit codes. Base scripts observed in `package.json`:
```bash
node --version
npm --version
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
```

Use real `Cargo.lock`/toolchain and local package scripts; failed infrastructure install is `BLOCKED_INFRA`, NOT a source PASS. Do not execute destructive migrations or production deploy; for Prisma migrations/rollback use authorized disposable DB with fresh isolated schema. Browser E2E must use actual configured runner and backend, not static screenshot. Check Redis queue/worker in safe environment. Perform DOC-E E1–E12 under proper approval; **E11 signed release and E12 production rollback cannot be manufactured or substituted by CI logs**. Report exactly which external gates remain blocked.

Tests must include at least: valid/invalid contract, unauthorized and wrong-role mutations, CSRF, session replay, OTAC brute force, idempotency/concurrent duplicate, transaction conflicts, worker retry/timeout and stale state, FREEZE consistency, incident/event/audit trace links, failure/partial-provider injection, persistent state after restart, migrations/rollback, UI failure state, deterministic serialization and artifact integrity.

**Stop falsely conflating levels:** Static check PASS != local full test PASS != current-HEAD CI PASS != production signoff.

## 06. TEMPORARY MEMORY AND CROSS-CHAT CONTINUATION

Before coding create local durable scratch directory **outside product tracked source** with:
`00_RUN_STATE.json`, `01_SPEC_INDEX.jsonl`, `02_REQUIREMENTS.tsv`, `03_SOURCE_LEDGER.jsonl`, `04_COMMAND_RESULTS.jsonl`, `05_TEST_MATRIX.jsonl`, `06_DEFECTS.jsonl`, `07_CHANGESET.jsonl`, `08_READY_QUEUE.jsonl`, `09_DECISIONS.jsonl`, `10_SKILLS_PROVENANCE.jsonl`, `11_FINAL_GATE.md`, `12_SNAPSHOT_HEAD.json`.
Follow exact content requirements in V5. After every real step, append record and readback; preserve superseded records, do not silently rewrite prior failure. Each record must include `original_spec_sha, P_locator, product_head, path/blob, command, exit, test_env, status, proof_link, negative_case, updated_at_source`. No invented agent/session IDs. Do not upload raw sensitive documents, secrets or confidential run logs to public AI-CONTEXT.
Write a unique per-execution handoff under `AI-CONTEXT/EVIDENCE/`; other chats start from the root START-HERE and readback exact files. Require an independent auditor to challenge the claimed gates when available. If no auditor, mark `INDEPENDENT_REVIEW_PENDING`.

## 07. MULTI-CHAT / WRITE CONCURRENCY

No shared global 'I am controller' assumption. Multiple chats may read, inspect, propose or test independently, but product mutation must have single-writer coordination. Right before push, compare against live HEAD; if stale, stop affected write and re-evaluate changed paths with the new base. Do not delete/merge/rename existing branches. The only intended source branch is `NEXY.ai`. AI-CONTEXT update is append-only unique file per task; preserve other writers.

## 08. STOP / SUCCESS CRITERIA

Stop an individual action on missing authority, stale/contended HEAD, denied access, a destructive production step without approval, security risk, conflicting requirement or missing validation.
Do not stop *all independent engineering* because one action is blocked.

**Only assert project 100% when:** complete source inventory + semantic review, exhaustive in-scope atomic spec matrix, source/run tests at exact current HEAD, current applicable CI, E1–E12 and all mandatory signoffs pass with unambiguous proof and no unreviewed exceptions. Count explicit denominators and attach evidence links. Otherwise status is `PARTIAL` or `BLOCKED`, never 100%.

At execution boundary write one compact handoff: current HEAD, exact files read, actual changes and commits, test commands/exits, PASS/FAIL/BLOCKED, unmet requirements sorted by ready/dependency, evidence links, known concurrent updates and next executable command. Never promise background continuation without a confirmed automation/runner.
