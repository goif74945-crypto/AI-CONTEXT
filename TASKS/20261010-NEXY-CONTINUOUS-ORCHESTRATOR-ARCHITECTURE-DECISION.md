# NEXY Continuous Engineering Orchestrator — Method Decision (PROPOSED / NOT DEPLOYED)
DATE: 2026-10-10 (Asia/Bangkok)
STATUS: DESIGN_ONLY / NO_WORKFLOW_INSTALLED / NO_PRODUCT_MUTATION
REFERENCE: COMMANDS/20261009-NEXY-GPT6-SOL-143-FIX-UNTIL-VERIFIED-V4.md

## OBJECTIVE
Operate a resumable hours-to-days engineering loop for DOC-C compliance using real source/test/audit evidence. No unsupported 100% claim.

## CHOSEN IMPLEMENTATION
Phase 1 (preferred first): GitHub Actions scheduled + manually dispatchable coordinator in AI-CONTEXT/main, OpenAI Responses API with exact model ID `gpt-6-sol`, independent audit model/role, persistent machine-readable checkpoint and bounded job execution. GitHub-hosted Actions per-job time limit: 6 hours, thus design shorter bounded slices that resume on next run. A scheduled trigger is not strictly continuous or guaranteed punctual; delayed/dropped runs require watchdog/recovery.
Phase 2 (ONLY if strict always-on scheduling is required after proving Phase 1): dedicated cloud VPS/always-on worker with persistent queue, watchdog and restart supervision; CI remains GitHub Actions. Runner/provider/service costs require explicit budget approval. DO NOT assume free Railway service is always-on.

## AUTHORITY AND LOCKS
- Read actual original NEXY-IGNIS DOCX; verify SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 before asserting DOC-C coverage. If original unavailable, label blocked requirements NOT_VERIFIED, continue safe independently verifiable work.
- Product repository goif74945-crypto/NEXY.AI- branch NEXY.ai ONLY. No Product mutation under this decision record. Future writes require explicit work authorization, head-safe single writer and exact-current-HEAD proof. No other Product branches/changes to permissions, secrets, protections, or workflows as a side effect.
- Control repository goif74945-crypto/AI-CONTEXT branch main: store durable queue, receipts, audit findings, checkpoints, and failures without confusing control metadata for Product implementation.
- Current authority command indicates 143 starting checks are gates, NOT 143 known defects and NOT the complete DOC-C denominator.

## ENGINEERING CYCLE
1. Read authoritative DOCX byte hash and live Product HEAD, lock requirement ID + exact source locator.
2. Pick a READY item from dependency-ordered queue; establish source+test baseline.
3. Builder develops minimal patch and negative/positive tests in an isolated runner workspace; tests must not touch production data.
4. Run focused tests, dependent regressions and applicable security/negative checks, preserving raw logs, exit codes, hashes.
5. Independent Auditor reviews source, tests, immutable result evidence and DOC-C mapping. Builder and Auditor must not independently write Product.
6. If authorized, single Product writer checks live branch HEAD and uses optimistic concurrency to apply only reviewed changes. Readback source/hash; reject stale HEAD. Otherwise store patch as PROPOSED only.
7. Append durable checkpoint in AI-CONTEXT; resume next READY item next run.

## FAILURE POLICY, BUDGET AND STOP CONDITIONS
- State machine: PENDING -> RUNNING -> PATCH_READY -> TESTED -> AUDITED -> COMMITTED_AND_READBACK (only if authorized); otherwise BLOCKED/FAILED/RETRYABLE.
- Crash/time limit/ratelimit: write last safe checkpoint and resume; retries limited with exponential backoff. No fabricated success and no endless retries of identical failing condition.
- Single-writer lease across processes PLUS optimistic HEAD validation; GitHub concurrency group alone is not cross-repository or cross-agent locking.
- Enforce maximum spend/tokens, tool requests, elapsed time per slice, maximum retries, secret-scoping, no live prod test writes and explicit KILL/PAUSE switches.
- Stop write action on ambiguous spec, wrong repo/branch, stale HEAD, missing authority, failing required test, unauthorized credentials, cost cap, missing release signoff or unsafe tool behavior; continue independent safe audits if possible.
- No 100% claim until exhaustive applicable atomic DOC-C inventory and evidence, required real regressions, external signoff where required, and independent audit pass.

## VERIFIED PLATFORM CONSTRAINTS (at decision time)
- OpenAI API models page lists `gpt-6-sol` for Responses API (GPT-6.1 Sol is separate/newer model ID).
- API billing is separate from ChatGPT subscription.
- GitHub-hosted Actions job execution time limit is 6 hours.
- GitHub scheduled workflows only run on default branch, can be delayed/dropped, and public repos may disable schedules after inactivity.
Sources:
https://developers.openai.com/api/docs/models/gpt-6-sol
https://docs.github.com/en/actions/reference/limits
https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform

## CURRENT REAL STATUS
Only this decision record is created. No agent runner, workflow, model API credential, billing configuration, Product edit/commit, or CI execution has been performed or verified in this chat.
