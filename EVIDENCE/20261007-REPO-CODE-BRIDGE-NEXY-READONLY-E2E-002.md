# Repo Code Bridge — NEXY.AI- read-only integration evidence

- Evidence date: 2026-10-07 (UTC)
- Scope: Repo Code Bridge Site only; `goif74945-crypto/NEXY.AI-` was not modified.
- Site version: 11
- Site source commit: `d2a52c0c12116b2fc01416e481cd402cef7b0e4f`
- Production deployment: `appgdep_6ac5eab9e3408191b1c7c28279fc4ca7` — succeeded
- Runtime environment revision: 8
- Production URL: https://repo-code-bridge.nexy-code-me.chatgpt.site

## Policy implemented

- Exact repository `goif74945-crypto/NEXY.AI-` is allowlisted for reads.
- Exact read-only branch: `NEXY.ai`.
- `prepare_change_set`, `commit_change_set`, and `ci_dispatch` fail closed with `REPOSITORY_READ_ONLY` HTTP 403.
- Other branches for the product repository fail closed with `BRANCH_NOT_ALLOWED` HTTP 403.
- Matching is exact; unrelated repository names containing similar text are not blanket-blocked.
- `open_vscode` returns URLs and verified head metadata; the Site does not launch local VS Code Desktop.

## Local verification

- `npm test`: PASS — 13 tests, 13 passed, 0 failed.
- `npm run lint`: PASS.
- `npm run build`: PASS.
- The publish workflow repeated test and build before version 11 was saved.

## Live Repo Code Bridge verification after version 11

- Runtime: GitHub `CONNECTED`; D1 `READY`; read/write/CI backend statuses `READY`.
- Catalog: 15 repositories; 1 read-only repository.
- Exact catalog entry: repository `goif74945-crypto/NEXY.AI-`; branches [`NEXY.ai`]; read=true; write=false; ci_dispatch=false.
- Repo status: default and selected branch `NEXY.ai`; head `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`; workflows `VERIFIED`; gateway write policy `DENY`.
- Repo read: `README.md` read successfully at the exact head above.
- Repo search: `DOC-C` returned 5 bounded results at the exact head; `SEARCH_SCOPE_PARTIAL` was reported and retained.
- VS Code handoff: https://vscode.dev/github/goif74945-crypto/NEXY.AI- returned with the same verified head and read-only policy.
- Negative mutation checks after deployment: prepare and CI both returned `REPOSITORY_READ_ONLY` HTTP 403; branch `main` returned `BRANCH_NOT_ALLOWED` HTTP 403.

## Browser and CI boundaries

- Chrome Direct Control device was online and pinged. The fixed Chrome Agent command started, but two status RPC attempts returned `EXECUTION_FAILED: fetch failed`; direct Chrome transport is therefore `NOT_VERIFIED`, not PASS.
- Authorized browser fallback opened the live Site, GitHub product repository on `NEXY.ai`, VS Code for Web, the GitHub Actions run page, and ChatGPT. VS Code visibly reported that the GitHub Repositories extension was not installed, so no installation was performed.
- Safe test-repository dispatch through Bridge was queued as run `37582850774` on `goif74945-crypto/repo-code-bridge-e2e-test`. GitHub marked it failed before steps because recent account payments failed or the spending limit needs to be increased. This is an external billing blocker; it is not evidence of a product-code failure.

## AI Role Court judgment

Execution mode: `LOGICAL_ISOLATION` (no platform sub-agent spawn/wait tools were exposed).

- Policy/architecture/build/test roles: PASS on the evidence above.
- Independent truth review: the read path and fail-closed mutation boundary are verified.
- Chrome Direct Control internal connector binding: NOT_VERIFIED.
- External GitHub Actions runtime pass: BLOCKED by account billing.
- Universal “100% perfect” claim: NOT_PERMITTED by the evidence contract.
- Overall judgment: `PARTIAL` with explicit blockers; no `TRUTH_PASS` seal.
