# NEXY.AI evidence-gated continuous source update policy V1

STATUS: ACTIVE_COORDINATION_POLICY / HUMAN_REQUEST_2026-10-10
SCOPE: Codex and collaborating AI chats working on goif74945-crypto/NEXY.AI- (existing canonical branch NEXY.ai), with AI-CONTEXT/main as the control archive.
AUTHORITY: This is **workflow policy**, NOT a replacement for the original NEXY-IGNIS DOCX, the product repo AGENTS.md, branch protection, security law or explicit owner approvals.
EFFECTIVE_AS: written instructions for agents that **actually read this file**. Saving it here does not silently reconfigure any bot or cause perpetual execution.

## 1. Continuous engineering obligation
- When an authorized Codex/build agent has an **active execution session**, it must maintain a live engineering queue and **continue successive real code-change / verify cycles** against unmet, source-grounded DOC-C obligations. Do not stop after producing a prompt, list or status report if a ready, safe actionable engineering task exists.
- **Product code must continually progress when improvement is demonstrably required, authorized and verifiable.** An update means a meaningful source modification with linked spec clause or reproducible defect, reviewable diff, positive and negative tests, exact HEAD evidence, and approved commit. **Do NOT create empty commits, arbitrary edits, fake activity, unnecessary refactors or a 'change every N minutes' timer.**
- If current code meets all provable obligations, retain it unchanged. Continue checks and evidence; code churn is not progress.
- An active session may stop at a genuine runtime boundary, tool failure, budget expiry or lack of authorized work; write resumable handoff instead of claiming background operation. For work while no Codex session is active, implement an **explicitly configured and authorized** job/CI/automation with real monitoring and confirmation. **No policy file alone provides autonomous continuous execution.**

## 2. Hard source identity and write fence
- Product repository: goif74945-crypto/NEXY.AI-; **only existing branch NEXY.ai** may receive authorized changes. This file is NOT direct authorization for this chat to modify product source. Other active builders must separately validate their assigned permission.
- Read current product AGENTS.md from live HEAD. Never create branch, fork or hidden branch; never rebase/force push, delete/rename branch, weaken protections, or change secrets/production without specific authorization.
- Before read/modify/commit, re-query current HEAD and exact source blob. Single-writer CAS / optimistic concurrency: reject stale writes; rebase **unpublished local change only** after evidence-based reconciliation; preserve peer changes; rerun affected tests before push.
- When a single path is locked by another chat, freeze that write and pick a nonconflicting task; never silently overwrite.
- AI-CONTEXT only holds planning, navigation, normalized safe evidence, run history and prompts. Do not treat it as proof that product code is correct, and do not put source secrets/credentials here. Append new evidence under unique path.

## 3. Navigation and authoritative interpretation
- Start from `NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.md` plus `.tsv`, check SHA and HEAD. Atlas has **88 navigation groups**, not 88 total atomic requirements.
- Original DOCX SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`; must verify actual bytes. P refs are **one-based paragraph numbers including empty paragraphs**, not page numbers.
- Authority final: DOC-C build, DOC-B system law, DOC-D where supported by DOC-C, DOC-E for deployment proof. Outside DOC-C scope/excluded is never silently promoted to required build. Exact sources and live current code overrule other AI reports.
- 143-check register and earlier audit reports are **discovery aids**, not a complete spec, not a current-head PASS record.

## 4. Required edit-and-test cycle (active session)
1. VERIFY: live HEAD, owner permissions, DOCX SHA and all relevant P refs; compare atlas path hints to live Git tree.
2. DETECT: derive one atomic build obligation or reproducible defect, ownership, dependencies, status `READY`, exact current-source proof.
3. RED: create or run a relevant failing test/assertion if meaningful (including adversarial, boundary, concurrency, regression and auth/security cases).
4. IMPLEMENT: smallest correct code change only; no fake mocks in production, placeholder implementations, weaker checks or invented APIs.
5. GREEN: run targeted tests, relevant integrations and full gates when environment permits; capture exact commands, exits and all failures.
6. SECURITY: ensure fail-closed behavior, auth/RBAC/CSRF/OTAC/idempotency, consistent FSM, storage integrity and system-law restrictions as applicable.
7. REVIEW: current-head source diff, changed-file SHA, no scope creep, no secret disclosure, conflict detection, rollback path.
8. COMMIT: only if authorized and PASS for required gates; **never claim success before GitHub confirms and readback verifies**. No new branch.
9. JOURNAL: append task id, P refs, old/new SHA, tests/runner/env/exit/proof in unique `AI-CONTEXT/EVIDENCE/` file; write exact-HEAD progress/handoff.
10. NEXT: re-query live product HEAD; advance next READY task. Blocked task is local, not a reason to abandon independent work.

## 5. What '100%' actually means
- 100% only when entire in-scope **atomic** DOC-C matrix and supported DOC-D/storage/auth obligations have matching current source, actual positive/negative/integration E2E proof, no unexamined conflict and no unresolved critical failure. Separate every denominator (source reads, substantive reviews, requirement acceptance, gate execution).
- E1–E12 under DOC-E each requires an actual evidence artifact with exact commit, command/test, environment, result, logs and authorized signoff where required. File existence, a test name or historical CI success is not proof.
- If Actions runner allocation, authorization or infrastructure blocks tests: classify `BLOCKED_INFRA` with IDs and errors; do not label code a pass/fail without executed proof. Continue available independent work.
- Do not deploy or migrate real production automatically. Real monitoring/signoff/deploy requires separate authorization; never weaken release policy to turn red CI green.

## 6. Multi-chat use, mandatory intake for participating agents
Any chat that is asked to participate must first read in this order:
1. `START-HERE-NEXY-IGNIS-CODEX-20261010.md`
2. This policy.
3. `NAVIGATION/20261010-NEXY-IGNIS-SPEC-TO-CODE-ATLAS-V1.md` and `.tsv`.
4. `COMMANDS/20261010-NEXY-CODEX-SPEC-EXACT-LONG-RUN-ENGINEERING-V5.md` plus latest explicitly designated successor.
5. Product `AGENTS.md` and current authenticated Git data.
Use each prior chat's records as leads and cross-check against source. Record a unique chat/run identifier if actually provided; do not invent one. Append only independent evidence, no overwrites.

## 7. Failure and stop
- Missing source authority / unknown SHA => STOP any affected spec-based mutation; retain unrelated READY tasks.
- Stale HEAD / conflicting peer edit => freeze affected commit and reconcile; no blind push.
- Unsafe network, credential, permissions, signed release uncertainty => freeze that action.
- Out of authorized work / execution no longer possible => write a resumable checkpoint and truthful final status. A paused worker **cannot be described as running continuously**.

STATUS SEMANTICS:
`SOURCE_LOCATED` ≠ `READ_FULL` ≠ `TESTED` ≠ `BEHAVIOR_VERIFIED` ≠ `RELEASE_APPROVED`.
