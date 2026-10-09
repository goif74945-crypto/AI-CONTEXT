# Repo Code Bridge batch-search performance and accuracy verification 003

Date: 2026-10-09 (UTC)
Status: PASS for every defined gate in this report

## Scope

Verify that Repo Code Bridge can read and search the complete eligible UTF-8 text surface of `goif74945-crypto/NEXY.AI-` quickly and accurately, with explicit coverage accounting, bounded GitHub requests, correct legacy line-number handling, live deployment provenance, and end-to-end use from ordinary ChatGPT Chat conversations.

The NEXY.AI- repository was read only during this verification. Its tested branch HEAD remained unchanged.

## Source changes

Repo Code Bridge source commits:

- `e74e72e3a2b213a75efe59fc58e7c51c883c576d` — batch repository blob reads through GitHub GraphQL with exact-SHA REST fallback.
- `e16a72b5cae90ab29737a6d0c88634402ab955f2` — correct line splitting and match line numbers for CRLF, LF, and bare-CR repository files.

Batch behavior:

- Deduplicates identical blob SHAs while preserving candidate order.
- Fetches GitHub blob text in bounded GraphQL batches.
- Classifies binary and truncated nodes explicitly.
- Falls back to the exact SHA through REST only for incomplete/missing/failed GraphQL nodes.
- Rejects unexpected REST encodings instead of silently treating them as text.
- Keeps coverage false if a candidate load fails.
- Separates the result limit from exhaustive inspection.

## Test-driven evidence

RED evidence:

- Missing batch-loader module caused the initial focused tests to fail.
- Unexpected REST encoding was initially accepted; the new fail-closed test failed before the fix.
- A bare-CR file `first line\rneedle line\rthird line` initially reported the match on line 1 instead of line 2.

GREEN evidence after fixes:

- `npm test`: 20 tests, 20 passed, 0 failed.
- `node --experimental-strip-types --test tests/repository-search.test.mjs`: 3/3 passed.
- `npx tsc --noEmit --incremental false`: passed.
- `npm run lint`: passed.
- `npm run build`: passed.
- `git diff --check`: passed.
- Source working tree was clean after commit/package.

Covered edge cases include GraphQL deduplication, partial fallback, isolated batch failure, invalid REST encoding, exhaustive scan with bounded returned results, failed/skipped coverage reporting, and bare-CR line numbering.

## Deployment provenance

- Site: Repo Code Bridge
- Site project ID: `appgprj_6ac56b9353f88191873e731529a5dc6f`
- Plugin ID: `plugin_asdk_app_sites_d587d513b07c81919ab4d36c35b9185e`
- Version: 15
- Version ID: `appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_e6f22d3621e48191a9c8487f0aa7b5d8`
- Deployment ID: `appgdep_6ac893d6d7708191a0371984933cac79`
- Deployed source commit: `e16a72b5cae90ab29737a6d0c88634402ab955f2`
- Archive SHA-256: `26163eece37e83b045ace8fa74a053257852e5290c84a85772663e8fabe24d26`
- Production status: `succeeded`
- MCP: enabled
- Environment revision: 9
- Live URL: https://repo-code-bridge.nexy-code-me.chatgpt.site
- Audience preserved: custom owner-only, one owner, zero external visitors.

## Live NEXY.AI- verification

Repository:

- `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Exact tested revision: `8ed9af89f68fb82f60d4a4f5ccbc06005ce91992`
- Revision before and after testing: unchanged

Match-heavy query `NEXY`, result limit 5:

| Metric | Value |
|---|---:|
| outer elapsed time | 9.451 s |
| candidate_files | 884 |
| inspected_files | 884 |
| searched_files | 882 |
| skipped_files | 2 |
| failed_files | 0 |
| matched_files | 303 |
| unique_blob_count | 882 |
| graphql_batch_requests | 45 |
| rest_fallback_requests | 0 |
| coverage_complete | true |
| results_truncated | true |
| warnings | RESULTS_TRUNCATED |

No-match query `__repo_code_bridge_no_match_batch_v15_20261009__`, result limit 1:

| Metric | Value |
|---|---:|
| outer elapsed time | 8.880 s |
| candidate_files | 884 |
| inspected_files | 884 |
| searched_files | 882 |
| skipped_files | 2 |
| failed_files | 0 |
| matched_files | 0 |
| unique_blob_count | 882 |
| graphql_batch_requests | 45 |
| rest_fallback_requests | 0 |
| coverage_complete | true |
| results_truncated | false |
| warnings | [] |

Fetch strategy reported by production: `GRAPHQL_BATCH_WITH_REST_FALLBACK`.
Coverage scope: `ELIGIBLE_UTF8_TEXT_BLOBS`.

Compared with the prior exhaustive implementation's 28–32 second worker time, the live v15 no-match traversal completed in 8.735 seconds of Worker wall time: approximately 3.2–3.7 times faster. The earlier historical implementation took about 68 seconds, making the current traversal about 7.8 times faster.

## Production runtime and logs

Runtime status:

- GitHub API: CONNECTED
- Credential: present
- D1: AVAILABLE / schema READY
- Read backend: READY
- Write backend: READY
- CI backend: READY
- Public search backend: READY
- Public fetch backend: READY
- Configured repositories: 15

Production log verification:

- Error events in the verification window: 0
- Full no-match search: HTTP 200, outcome `ok`
- Worker wall time: 8735 ms
- Worker CPU time: 133 ms
- Worker script version: `edbba701-c6bf-4d5d-a7f4-4edf8b97638c`
- Request ID: `857374e8f63e598a97d7a0f640847747`

## Ordinary ChatGPT Chat end-to-end evidence

Both conversations were created from ordinary ChatGPT Chat with the composer showing `Chat=1` and `Work=0`. Repo Code Bridge was explicitly selected from the `@Repo` plugin picker; the prompts were not issued from a Work chat.

Primary conversation:

- Chat: `https://chatgpt.com/c/6ac8947b-8668-83ec-972b-2a1b41d3c98a`
- Plugin link resolved to the preserved plugin ID.
- The answer reported: 884 candidates, 884 inspected, 882 searched, 2 skipped, 0 failed, coverage true, 45 GraphQL batches, 0 REST fallbacks, and the first 3 real matches.
- It explicitly verified `inspected_files = candidate_files`, `failed_files = 0`, and `coverage_complete = true`.

Independent audit conversation:

- Chat: `https://chatgpt.com/c/6ac894c5-7240-83ec-a919-0515c81f1088`
- Used a no-match sentinel query.
- Returned `AUDIT RESULT: PASS`.
- Verified matched 0, failed 0, coverage true, results_truncated false, warnings empty, 884/884 inspected, 882 searched, 2 skipped, 45 GraphQL batches, and 0 REST fallbacks.

## Final gate matrix

| Gate | Result |
|---|---|
| Focused regression tests | PASS |
| Full tests | PASS (20/20) |
| Typecheck | PASS |
| Lint | PASS |
| Production build | PASS |
| Diff integrity | PASS |
| Exact source/version provenance | PASS |
| Private owner-only audience preserved | PASS |
| Runtime backends | PASS |
| Exhaustive eligible-text coverage | PASS |
| No failed file reads | PASS |
| Match-heavy correctness | PASS |
| No-match correctness | PASS |
| Bounded GitHub batch fetch | PASS |
| No unnecessary REST fallback | PASS |
| Production errors | PASS (0) |
| Ordinary Chat, not Work | PASS |
| Independent ordinary-Chat audit | PASS |
| NEXY.AI- remained unmodified | PASS |

## Conclusion

Every explicitly defined test, build, deployment, runtime, coverage, performance, line-number, production-log, and ordinary-Chat end-to-end gate in this report passed. This is evidence for the tested source commit, deployed version, exact NEXY revision, and recorded queries; it is not a claim that unknown future inputs can never expose another defect.
