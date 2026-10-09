# Repo Code Bridge exhaustive-search fix and production validation

Date: 2026-10-09 UTC

## Scope

Validated Repo Code Bridge against the immutable NEXY.AI- revision without modifying the product repository.

- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Exact revision: `8ed9af89f68fb82f60d4a4f5ccbc06005ce91992`
- Site source commit: `e2539ba21154d5a248b6d16d5505a04f20797b13`
- Saved Site version: `appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_6df04679945c8191b74f17e62b256822`
- Production deployment: `appgdep_6ac87a6ced24819187dc1fb1412cbed0`
- Production URL: https://repo-code-bridge.nexy-code-me.chatgpt.site

## Defects corrected

1. `repo_search` stopped scanning as soon as the returned result list reached `max_results`; result limiting incorrectly reduced repository coverage.
2. Search did not distinguish returned-result truncation from incomplete file coverage.
3. Search did not report candidate, inspected, skipped, failed, and total matched counts.
4. Cloudflare environment types omitted `READ_ONLY_REPOSITORIES` and `READ_ONLY_BRANCHES`, causing `tsc --noEmit` to fail.
5. README claimed unconditional read-only access while the deployed policy has an explicit exact-branch write/CI exception.

## Implementation

- Added a bounded-concurrency exhaustive text-candidate scanner.
- `max_results` now limits only the returned match list.
- Search now reports `candidate_files`, `inspected_files`, `searched_files`, `skipped_files`, `failed_files`, `failed_paths`, `matched_files`, `coverage_scope`, `coverage_complete`, `results_truncated`, and explicit warnings.
- Deterministic candidate order is preserved in returned results.
- Tree truncation and file failures cause a partial coverage verdict; result truncation alone does not.
- Added regression tests for result-limit independence and skipped/failed-file accounting.

## Local verification

All gates passed on the exact deployed source:

- Unit/integration tests: 16/16 passed
- TypeScript: `npx tsc --noEmit` passed
- ESLint: `npm run lint` passed
- Production build: `npm run build` passed
- `git diff --check` passed

## Production proof: match-heavy search

Input: `repo_search(query="NEXY", max_results=5)`

- candidate_files: 884
- inspected_files: 884
- searched_files: 882
- skipped_files: 2
- failed_files: 0
- matched_files: 303
- coverage_complete: true
- results_truncated: true
- warnings: [`RESULTS_TRUNCATED`]

This proves the tool inspected all 884 candidates while returning only five matches.

## Independent normal-ChatGPT auditor proof

A separate ordinary ChatGPT chat (Chat mode, not Work mode and not a project chat) explicitly selected `@Repo Code Bridge` and ran:

1. `repo_status` on branch `NEXY.ai`.
2. `repo_search` on the exact revision with the guaranteed-no-match query `__repo_code_bridge_no_match_audit_20261009__` and `max_results=1`.

Observed:

- HEAD matched exactly.
- candidate_files: 884
- inspected_files: 884
- searched_files: 882
- skipped_files: 2
- failed_files: 0
- matched_files: 0
- coverage_complete: true
- results_truncated: false
- warnings: []

Auditor verdict: `AUDIT_PASS`.

The first untagged ordinary-chat attempt correctly failed closed because no plugin was attached. Selecting `@Repo Code Bridge` in the composer resolved discovery and produced tool-backed results.

## Runtime evidence

- Deployment status: succeeded
- MCP capability: ready
- Recent production error log query: zero error events
- Successful exhaustive MCP calls returned HTTP 200.
- Worker wall times observed for full-project searches were approximately 28–32 seconds; CPU time remained approximately 1.0–1.8 seconds.
- Previous implementation's no-match baseline took approximately 68 seconds and returned `SEARCH_SCOPE_PARTIAL`.

## Verdict

All defined gates for this change passed. Repo Code Bridge now reads and searches the complete eligible UTF-8 text scope of the tested NEXY.AI- revision, separates coverage from result truncation, and fails closed when coverage cannot be proven.
