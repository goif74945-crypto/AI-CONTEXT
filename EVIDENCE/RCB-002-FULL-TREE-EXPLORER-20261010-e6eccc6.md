# RCB-002 Full Tree Explorer — source/deployment evidence

Date: 2026-10-10 Asia/Bangkok
Control repository: goif74945-crypto/AI-CONTEXT
Control branch: main
Fresh AI-CONTEXT HEAD immediately before append: 110da12ec9ca78e83708910a524dc4b5b7bc9f2a

## Source provenance

- Authoritative Site source branch: main
- v18 baseline: 4917c6c99cbf7b878c55ac41446363e90b4770c4
- New source commit: e6eccc6e0fd210b6f690fdb535e6a816a14f82c3
- Parent commit: 4917c6c99cbf7b878c55ac41446363e90b4770c4
- Source remote HEAD was re-read immediately before push as 4917c6c99cbf7b878c55ac41446363e90b4770c4.
- Source remote HEAD was re-read immediately before private publication as e6eccc6e0fd210b6f690fdb535e6a816a14f82c3.
- Changed paths:
  - app/mcp/route.ts
  - lib/gateway.ts
  - lib/github.ts
  - lib/repository-tree.ts
  - tests/repository-tree.test.mjs
- Commit blob SHAs:
  - app/mcp/route.ts = cbd25f707d570ec0de286637e1132e581fe109e8
  - lib/gateway.ts = 7da820803febac9a72af30ef8329d32dee589915
  - lib/github.ts = 182fc42e877248e730030da34b8baea02b023467
  - lib/repository-tree.ts = ba745dd1b5662701383c874e3275a2f2c2c3fc67
  - tests/repository-tree.test.mjs = 44da50dfc3a0a2a4a0845c2ae25c8f8314e05d16

## RCB-002 audit and implementation

v18 had no repo_tree MCP definition, no gateway handler, and only a recursive getTree call used internally by repo_search. The smallest compatible addition was:

- exact full 40-hex commit revision validation and returned commit-SHA verification;
- non-recursive Git tree-page requests, depth-first recursive traversal, deterministic path/mode/SHA ordering, and bounded pages (max 100 entries);
- stable continuation handles carrying repository, exact revision, path prefix, root tree SHA, and directory offsets;
- provider truncation, provider SHA mismatch/invalid response, provider errors, continuation-state limit, and bounded diagnostic reporting as explicit incomplete states;
- normalized relative paths with traversal/backslash/empty-segment rejection;
- accurate blob/tree/commit metadata, including modes 100644, 100755, 120000 symlink, and 160000 submodule; symlinks/submodules are never traversed;
- existing tools and deny-by-default write/workflow/CI policy preserved.

No arbitrary-large synchronous completeness claim is made.

## Tests and checks

- Focused RCB-002 tests: 6/6 passed, exit 0, duration 295.253235 ms.
- Full pnpm test: 34/34 passed, exit 0, duration 327.556412 ms.
- pnpm lint: exit 0.
- pnpm build: exit 0.
- git diff --check: exit 0.
- Tests cover empty tree, deterministic pagination, revision-bound stale cursor, provider truncation, unsafe input/provider paths, Git modes, and partial provider errors.
- No production performance gain is claimed.
- goif74945-crypto/NEXY.AI- was not modified.

## Publication

- Site version: 19
- Version ID: appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_79fbb24370108191aaae56a9fe1622b9
- Deployment ID: appgdep_6ac9fa11cd8c819199db1730bf203171
- Deployment status: succeeded
- Source mapping: e6eccc6e0fd210b6f690fdb535e6a816a14f82c3
- Local archive SHA-256: 4e0fd60cd580413470448b306bd677bce25e390da336c813e495262ec77dc127
- Server archive hash: sha256:46dc6075b6fddfaa73025f6c3a265e0aaf331ee053d78819d1876e8c3c5569a8
- Live URL: https://repo-code-bridge.nexy-code-me.chatgpt.site
- MCP URL: https://repo-code-bridge.nexy-code-me.chatgpt.site/mcp
- Access: custom owner-only; allowed account user count 1, group count 0, external visitor count 0.
- Unauthenticated live GET: HTTP 401.
- Authenticated live repo_tree probe: HTTP 401 Unauthorized; direct live tree execution is UNVERIFIED.

## Evidence append integrity

A fresh AI-CONTEXT HEAD was read immediately before this unique-file append. The available create-file append route does not expose an expected_sha/CAS parameter, so this records fresh-head verification plus unique-path creation, not a stronger parameterized SHA lease.

## Verdict

RCB-002 source implementation and automated checks: VERIFIED for committed source.
Private Site source mapping, deployment, and access policy: VERIFIED.
Authenticated live repo_tree invocation: UNVERIFIED due runtime authorization boundary.
Production-scale performance improvement: NOT CLAIMED.
