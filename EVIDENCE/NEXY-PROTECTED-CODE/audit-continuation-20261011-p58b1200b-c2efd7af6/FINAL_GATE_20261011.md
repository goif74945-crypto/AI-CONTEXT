# NEXY Exact Spec Audit V1 — append-only independent continuation (2026-10-11)

**Final decision: NOT_100_PERCENT_VERIFIED**. **Protected units: 0**. NEXY.AI- product source changed: **0 files/commits**.

## Immutable authorities
- Product repository: `goif74945-crypto/NEXY.AI-`, canonical branch `NEXY.ai`, current HEAD when checked: `58b1200bd61b867e917057d0019eea78ea9f6b2a`.
- Git commit tree SHA: `6fd81ae8150aecc341f8a49f65e3c050f559c51f`, 889 blobs / 203 directories / 1,092 total Git tree entries, truncated=false.
- Actual original-byte DOCX SHA-256 verified: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`, size 2,146,350 bytes, 12,537 paragraphs (including blank). Full original P-index is in the local temporary journal, not copied into AI-CONTEXT.
- Effective law: actual DOCX and owner instructions, product AGENTS/permissions, NEXY policies; old atlas and 143 checkpoints are navigation only.

## Source and spec audit coverage
- Per-path full source-content response receipts reconciled against exact Git blob SHA: **145 / 889 unique blobs**. Pending directly full-read source content: **744 / 889** (exact paths and SHAs in `PENDING_744_SOURCE_PATHS.tsv`). This is **content-retrieval coverage only**, not semantic examination or spec fulfillment.
- Full semantic verification across all 889: INCOMPLETE; semantic certified unit count 0. Complete atomic requirement denominator: UNKNOWN. DOC-C has 612 nonblank paragraphs, which are not necessarily 612 atomic obligations.
- DOC-C P9912–P9949 26 numeric defaults: 26/26 static source literal values matched; consumers, overrides and actual behavior NOT VERIFIED. DOC-C P10353–P10469 FSM: all 12 explicit required matrix rows statically found and fatal->STOP for seven pre-STOP states; runtime guards, incident creation and audit emission NOT VERIFIED.
- DOC-D 12 screen groups and 14 named components were source-read with actual blobs; Browser E2E NOT_RUN. 38 API route source files inspected as content receipts; 12 canonical routes identified, additional 26 require independent scope/auth/security verification, not presumed failure.

## Negative findings with exact limitations
- `packages/auth/otac.ts` blob `bb6134ab1946c8cfa8f130eb7eea5a777d02c58e`: `safeEqual` has JavaScript-vs-UTF8 length exception behavior; `computeDeviceId` tuple concatenation collisions. Isolated copied-expression Node 22.16.0 test 5 cases, 2 PASS / 3 FAIL, exit 1; log SHA-256 `e0e340ad765b911c24253c58533d6de8624b785e6dc60cbfc634f59c9109396a`. NOT a production exploit proof or actual repository module test; production session binding imports different helpers.
- Repo Code Bridge content scanner skipped `package-lock.json` (262144-byte limit) and `packages/lo2/engine.ts` (8 NUL bytes). Exact-head GitHub fetch_file fallback read both full bytes and matched exact source blob SHA; NULs are inside template-literal field delimiters, behavioral effect UNVERIFIED. Scanner coverage_complete remains false, even though alternative reads succeeded.
- At exact HEAD, four GitHub Actions workflow runs `37899764374`, `37899764452`, `37899764383`, `37899764371` show failure. Selected job steps=[] and job logs returned 404 BlobNotFound, so root cause UNKNOWN, not assumed code failure. No native project npm/Vitest/DB/Cargo/Browser E2E tests executed by this audit; isolated environment has no full git checkout (github.com DNS failure), no cargo.
- Twelve `docs/evidence/current/E01..E12` product files read; all referenced old source commit `0d0d82bdc7d04ef8248f310d106cf5e4c1dd7a3d`, not current HEAD. E11 explicitly records operator NONE, BLOCKED_EXTERNAL signoff. Every DOC-E E1–E12 gate at current HEAD remains **NOT_VERIFIED**, including E11 release approval. Alternate receipt elsewhere not exhaustively searched; do not assert absolute absence.

## Registration and protection
- PROTECTED events created by this audit: **0**; no smallest unit has full, current-head atomic-spec acceptance, positive+negative+integration proofs, direct dependencies and independent adversarial review. Prior policy instructions exist in AI-CONTEXT; they apply to participating agents but are NOT server-side enforcement.
- GitHub NEXY.ai `protected=false`, branch protection `enabled=false` from read-only branch API. Rulesets GET 403 plan/access error; current ruleset state UNKNOWN. `POLICY_INSTRUCTIONS_SAVED=true`; `GITHUB_ENFORCEMENT_CONFIGURED_BY_THIS_AUDIT=false`.
- Earlier reconciliation V1 incorrectly undercounted 26 complete receipts without per-row revision metadata. V2 reanchors by unchanged Git blob SHA on this exact Git tree, explicitly preserves error history and leaves one nonexistent wrong-path receipt invalid; V2 counts 145 distinct verified content receipts. No peer file overwritten.

## Resumable change request rule for authorized builders
Read current HEAD and active protection evidence; cite original DOCX P-number or reproducible defect, affected exact symbol/contract and blob SHA; require smallest diff, transitive impact analysis, owner-specific authorization for changing a protected unit, authentic positive/negative/integration/regression test logs, rollback and independent review. Freeze affected writes on missing proof; never bypass branch protections or change product source under this read-only audit.

## Remaining work (incomplete, not fake-pass)
744 full source content receipts pending; complete semantic traversal and binary/generated classifications; full original atomic spec extraction/conflicts; authorized native tests with database/queue/browser/Rust; same-HEAD DOC-E E1–E12 proof and authorized signoff; independent adversarial reviewer. This checkpoint DOES NOT claim completion or background work.
