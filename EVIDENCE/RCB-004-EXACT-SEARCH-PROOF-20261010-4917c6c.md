# RCB-004 Exact Search Proof — source/deployment evidence

Date: 2026-10-10 Asia/Bangkok
Control repository: goif74945-crypto/AI-CONTEXT
AI-CONTEXT branch: main
Fresh AI-CONTEXT HEAD immediately before append: 0088b1a1b2f2b5df7da07aadab60960b1dd1d907

## Source provenance

- Site v17 baseline commit: 68f90dce25494d245fccc0ac1dee1b737d77094c
- Site source branch: main
- Source remote HEAD after push: 4917c6c99cbf7b878c55ac41446363e90b4770c4
- Parent commit: 68f90dce25494d245fccc0ac1dee1b737d77094c
- Changed source/test paths:
  - app/mcp/route.ts
  - lib/gateway.ts
  - lib/repository-search.ts
  - tests/repository-search.test.mjs
- Exact new blob SHAs:
  - app/mcp/route.ts = 4cc3bce2fc8b4dd3d644aebe7e9784a0d96711d2
  - lib/gateway.ts = 793a11615685a6ab20150f80dc8651cf4dc3e2dc
  - lib/repository-search.ts = 209a1e0b66759fdfabd729cc2b8148d473236a81
  - tests/repository-search.test.mjs = 0c3da4e0dec8cbeb744b2b18812394c4b9d31203

## RCB-004 source changes

- Search results now expose per-result provenance binding repository, exact revision, blob SHA, path, and line evidence.
- Candidate enumeration, inspection, and eligible-text coverage are reported separately.
- Skipped paths include reasons; failed/skip diagnostic arrays are bounded with explicit truncation flags and warnings.
- max_results only bounds returned results; all candidates are still inspected.
- Provider request counts remain exposed, with a grouped provider_requests object.
- duration_ms is measured for the repo_search operation.
- index_revision=null and index_status=NOT_USED because no search index exists.
- cache_status=NOT_USED because no search cache exists.
- MCP repo_search schema now requires a full 40-hex commit SHA pattern.
- coverage_complete is false when the tree is truncated, content is skipped, or file loading fails.

## Checks

- Focused repository-search test: exit 0, 5/5 passed.
- Full pnpm test: exit 0, 28/28 passed; duration 313.543944 ms.
- pnpm lint: exit 0.
- pnpm build: exit 0.
- git diff --check: exit 0.
- No production performance gain claimed.
- No mutation was made to goif74945-crypto/NEXY.AI-.

## Publication

- Site version: 18
- Version ID: appgprj_6ac56b9353f88191873e731529a5dc6f~appgver_421c3d4e3bd48191ba7196331c5738ea
- Deployment ID: appgdep_6ac9f611033481919f4f2a076f083b7f
- Deployment status: succeeded
- Source mapping: 4917c6c99cbf7b878c55ac41446363e90b4770c4
- Archive server hash: sha256:b2e3afcadd1e5e1291338cb521fdc2796be03b84194f9e355ce1dcdda42487ca
- Live URL: https://repo-code-bridge.nexy-code-me.chatgpt.site
- MCP URL: https://repo-code-bridge.nexy-code-me.chatgpt.site/mcp
- Access: custom owner-only; one allowed owner, zero groups, zero external visitors.
- Live page: Gateway ONLINE, GitHub CONNECTED, D1 READY, truthful Read/Write/CI UNVERIFIED_REMOTE_PERMISSION.
- Unauthenticated live HTTP request: 401.
- Direct authenticated MCP runtime_status curl: Unauthorized in this environment; not claimed as verified.

## Verdict

RCB-004 source implementation and automated checks: VERIFIED for the committed source.
Private Site deployment/source mapping/access: VERIFIED.
Direct authenticated live MCP tool invocation: UNVERIFIED.
Production-scale performance improvement: NOT CLAIMED.
