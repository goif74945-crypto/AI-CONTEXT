# ACTIVE CLAIM — T-S9-REVPAGE-4C71B8D2

- CHAT_ID: C-SOL-20261006-S9-REVPAGE-4C71B8D2
- PROJECT: NEXY.AI / NEXY-IGNIS
- SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
- INTEGRATION_BRANCH: NEXY.AI-Test-AI
- BASE_SHA: aec9afaa77213c37b223b7594b92eb81c7862f9a
- WORKER_BRANCH: work/NEXY-AI-Test-AI/T-S9-REVPAGE-4C71B8D2
- STATUS: AWAITING_VALIDATION
- MUTATION_SCOPE:
  - apps/web/app/vault/[id]/page.tsx
  - tests/contract/revision-history-pagination.test.ts
- REQUIREMENT_BINDING:
  - DOC-D §6.1 S9 Revision History: Compare Revision / Restore
  - DOC-D §6.4 RevisionTable columns and actions
  - DOC-C GET /api/artifacts/:id/revisions cursor-pagination principle; product revision-view already exposes compatible next_cursor
- GAP:
  - S9 requests only the first revision-view page (default max 100) and ignores next_cursor.
  - revision-view sorts ascending, so artifacts with >100 revisions hide newer truth.
  - the UI labels the last two loaded rows as LATEST REVISION COMPARISON even while newer pages may exist.
- REQUIRED_BEHAVIOR:
  - preserve current server authority and cursor contract.
  - expose bounded LOAD MORE continuation using next_cursor.
  - append new pages without discarding already loaded rows.
  - never claim LATEST REVISION COMPARISON until the final page is loaded.
  - keep restore/export behavior unchanged.
- FORBIDDEN:
  - no NEXY.ai mutation.
  - no direct NEXY.AI-Test-AI mutation.
  - no new backend write authority.
  - no fabricated runtime/test evidence.


## Candidate evidence — 2026-10-06
- PR: https://github.com/goif74945-crypto/NEXY.AI-/pull/83
- CANDIDATE_SHA: bc9012021ee4cb4ef738ac684554bdded850ca9a
- PR_BASE_SHA: 0eb26e46839232ddb5272c6c1f6cff2331248823
- BASE_WORKER_SHA: aec9afaa77213c37b223b7594b92eb81c7862f9a
- COMPATIBILITY: touched existing page blob was unchanged between worker base and PR base; second changed file is new.
- STATIC_DIFF: 2 files only; S9 cursor continuation + isolated contract oracle.
- VALIDATION_STATUS: BLOCKED_INFRA; exact candidate has 0 workflow runs and 0 commit statuses.
- TEST_CLAIM: NONE. Static review only.
- GLOBAL_RUNNER_CONTEXT: exact-head validation blocker is already owned in AI-CONTEXT; do not duplicate CI infrastructure work.
- INTEGRATION_DECISION: FAIL_CLOSED. Do not merge until exact-candidate test evidence exists.
