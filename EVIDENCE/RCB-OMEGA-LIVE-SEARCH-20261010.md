# RCB Omega live exact-search verification addendum

Task ID: RCB-OMEGA-LIVE-SEARCH-20261010
Date: 2026-10-10
Scope: append-only correction/extension to the v18 deployment evidence.

## Live authenticated tool call

After Site v18 deployed, the configured Repo Code Bridge MCP connector completed an actual `repo_search` call against the production gateway:

- Site version: 18
- Source commit: 4917c6c99cbf7b878c55ac41446363e90b4770c
- Deployment: appgdep_6ac9f611033481919f4f2a076f083b7f (succeeded)
- Repository: goif74945-crypto/AI-CONTEXT
- Exact revision: 8530a837a104444e7bec2f755b2115c4aa2a6139
- Query: `coverage_complete`
- Path prefix: `EVIDENCE`
- max_results: 1
- Result: one match at `EVIDENCE/20261010-NEXY-EX018-HEAD-BOUND-INDEPENDENT-AUDIT-INTERIM-GATE-REPORT.md`, line 8
- Result blob SHA: `f8f967f16147ebaef415b0519d66157bcaa0bf3e`
- candidate_files / inspected_files / searched_files: 130 / 130 / 130
- skipped_files / failed_files / matched_files: 0 / 0 / 1
- coverage_scope: `ELIGIBLE_UTF8_TEXT_BLOBS`
- candidate_enumeration_complete / inspection_complete / coverage_complete: true / true / true
- results_truncated: false
- GraphQL batch requests / REST fallbacks: 7 / 0
- duration_ms: 1589 (single observed query; not a performance benchmark)
- index_status / cache_status: `NOT_USED` / `NOT_USED`
- warnings: none
- Production audit log read-back: `repo_search goif74945-crypto/AI-CONTEXT PASS` at 2026-10-10 08:25:09 UTC

This verifies a live authenticated connector tool execution and the v18 exact-search response contract. A separate raw HTTP curl to `/mcp` from the source-editing environment returned Unauthorized; that transport limitation remains distinct and no claim is made that the raw curl succeeded.

A first probe with a trailing slash in `path_prefix` returned `PATH_INVALID`; the successful retry used the normalized relative prefix `EVIDENCE`. No repository writes occurred during either search.

## Evidence repository provenance

Appended to AI-CONTEXT/main using a fresh branch HEAD read and compare-and-swap update. This record supplements, and does not rewrite, earlier append-only evidence.
