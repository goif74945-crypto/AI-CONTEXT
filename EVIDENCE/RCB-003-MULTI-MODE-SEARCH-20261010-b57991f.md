# RCB-003 Multi-Mode Search — 2026-10-10

## Scope and provenance

- Site: Repo Code Bridge, private owner-only Site project `appgprj_6ac56b9353f88191873e731529a5dc6f`
- Authoritative source repository: `a0e48c8f-e290-43d2-857c-4756a4fb53fd/appgprj_6ac56b9353f88191873e731529a5dc6f`
- Baseline branch: `main`
- Audited baseline/deployed v19 source: `e6eccc6e0fd210b6f690fdb535e6a816a14f82c3`
- Source commit produced by this slice: `b57991f72e06f341ebebe4a5db0a9be1fac9b38d`
- Parent commit: `e6eccc6e0fd210b6f690fdb535e6a816a14f82c3`
- Remote `main` was read immediately before push at `e6eccc6e0fd210b6f690fdb535e6a816a14f82c3`; non-force push completed fast-forward to `b57991f72e06f341ebebe4a5db0a9be1fac9b38d`; post-push `ls-remote` matched that commit.
- Protected repository `goif74945-crypto/NEXY.AI-` was not written.

## Audit finding

The v19 source had only exact-40-hex-revision literal UTF-8 blob search. It enumerated the provider tree, fetched eligible blobs, reported exact repository/revision/path/blob/line provenance, separated candidate/inspected/searched/skipped/failed/matched counts, and kept max_results as a returned-result bound. No symbol, semantic, history, dependency, regex, or path-glob mode was present in the source or MCP contract. No authoritative RCB-003 contract outside the current source was found in the available AI-CONTEXT search.

## Implemented smallest compatible slice

Added optional MCP `repo_search.mode` with enum `literal | path_glob`, defaulting to `literal` so existing calls and behavior remain compatible.

- `literal`: existing exhaustive UTF-8 content/path substring scan.
- `path_glob`: bounded normalized Git path matching only; supports `*`, `?`, and `**` only as a complete path segment.
- Glob input is rejected for empty, oversized (>256), absolute, backslash, NUL/control, traversal/empty segments, unsupported regex/glob syntax, or embedded double-star syntax.
- Path-glob mode scans every eligible tree blob candidate before applying `max_results`; it does not fetch content and reports `coverage_scope=ELIGIBLE_GIT_TREE_PATHS`, exact revision/blob/path provenance, zero content-provider requests, result truncation, and tree-enumeration incompleteness truthfully.
- No symbol/semantic/history/dependency capability is claimed.
- Index and cache facts remain explicitly `NOT_USED`/null; no performance claim was made.

## Changed source/test paths and blob SHAs

| Path | New blob SHA | Parent blob SHA |
|---|---|---|
| `app/mcp/route.ts` | `0ea86c5bce972914568678a03eec757c836e825f` | `cbd25f707d570ec0de286637e1132e581fe109e8` |
| `lib/gateway.ts` | `db2bf324aff78ced480585ea97a7ed0891d12013` | `7da820803febac9a72af30ef8329d32dee589915` |
| `lib/repository-search.ts` | `a78831e2ae7207aa79a8bfd2986aef57a8c12f56` | `209a1e0b66759fdfabd729cc2b8148d473236a81` |
| `tests/repository-search.test.mjs` | `e36daffecfd8ee7fdb07c1d73473119e9892eefb` | `0c3da4e0dec8cbeb744b2b18812394c4b9d31203` |

## Tests and checks

- Targeted search tests: `pnpm test -- --test-name-pattern='path glob|repository search'` — exit 0; 37 selected/available tests passed in the project run.
- Full tests: `pnpm test` — exit 0; 37 passed, 0 failed.
- Lint: `pnpm lint` — exit 0.
- Build: `pnpm build` — exit 0.
- Diff check: `git diff --check` — exit 0 before and after commit.
- Adversarial coverage added: bounded result truncation with exhaustive candidate inspection, Unicode paths, no-match, traversal/absolute/backslash/control rejection, unsupported regex/glob syntax, oversized glob, and incomplete provider enumeration. Existing real tests continue to cover stale exact revision validation, deny-by-default permissions including protected NEXY.AI- read-only behavior, blob partial failures, and tree pagination/provider truncation.
- Final worktree was clean.

## Site publication and verification

- Archive: `/workspace/scratch/91a25299b5e1/rcb-omega-b57991f-root-v20.tar.gz`
- Local archive SHA-256: `459108d8cddc28f9593920a8019ca62132df7ea1905c5feeb391ae64a9826d42`
- Site-normalized archive hash: `sha256:45341c22dccddb7b7bb809d4e9dd795b49c0b5af146b1bd598b6016d6e03d97b`
- Site version: 20
- Version ID: `appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_ab3515dc7c4c8191b8eccd671ee0879e`
- Deployment ID: `appgdep_6ac9fc3350d881918b0b0c8dad4b2d95`
- Deployment status: `succeeded`
- Live URL: `https://repo-code-bridge.nexy-code-me.chatgpt.site`
- Version readback source mapping: `b57991f72e06f341ebebe4a5db0a9be1fac9b38d`
- Access readback: `custom`, current user `owner`, allowed account user IDs exactly `d7aa6bae-6933-41ae-96f9-fc6ede2d2152`, zero external visitors, zero groups.
- One bounded production `repo_tree` read-only MCP probe was attempted against exact revision `67a0e4cdbe44d66614fd5a51218592bb18abbf60` with `max_entries=2`; endpoint returned HTTP 401 Unauthorized. Live tool behavior is therefore unverified, not claimed successful.

## Remaining blocker / next requirement

The source and available contract do not provide an authoritative ordered RCB requirement map beyond this slice, and no production-authenticated MCP probe was available (401). The next high-priority implementation slice should be selected only after a fresh source/contract audit; no unsupported search modes or production performance claims are asserted.

## AI-CONTEXT append note

Fresh AI-CONTEXT branch HEAD read immediately before this unique-file append: `e6666f0e265d07e923efbebddf6ca771ad6023ca`. The authorized `github_create_file` route has no expected-SHA/CAS argument; this append therefore uses the fresh-head read plus a unique path and records that exact CAS was unavailable at the connector boundary.
