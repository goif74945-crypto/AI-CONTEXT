# NEXY.AI- old ZIP vs current NEXY.ai: evidence-led specification comparison
Date: 2026-10-10 (Asia/Bangkok)
Mode: READ_ONLY_PRODUCT / AI_CONTEXT_REPORT_WRITE_ONLY / NO_FAKE_PASS

## Fixed provenance

- Product repository: `goif74945-crypto/NEXY.AI-`. No product mutation was made in this audit.
- Old snapshot: user-supplied `NEXY.AI--NEXY.ai.zip`.
- Independently rebuilt Git root tree SHA of *all* old ZIP contents: `a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c`.
- Old GitHub commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`; GitHub commit's tree SHA independently matches the rebuilt old ZIP tree.
- Current branch `NEXY.ai`, observed and pinned HEAD: `58b1200bd61b867e917057d0019eea78ea9f6b2a`. This is a point-in-time reference only; re-query before subsequent work.
- Original authority file: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20261008-072414).docx`, independently hashed SHA256 `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`; 12,537 paragraphs; 10,979 nonempty.
- Authority: DOC-C is BUILD, DOC-E DEPLOY; source presence alone must never be promoted to DOC-C semantic acceptance or DOC-E deployment approval.

## Confirmed structural comparison

| Metric | Old | Current |
| --- | ---: | ---: |
| Git file blobs | 881 | 889 |
| Source delta from old | baseline | 8 commits ahead; 13 modified; 8 added; 0 deleted |
| Unchanged old blob paths | 881 | 868 |

Source: https://github.com/goif74945-crypto/NEXY.AI-/compare/9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43...58b1200bd61b867e917057d0019eea78ea9f6b2a

Key changed code: `packages/api/auth.ts` (OTAC claim boundary), `packages/core/canonical-json.ts` (fail-closed domain checks), `packages/law/prerelease.ts` (quorum cardinality), `packages/queue/retry-policy.ts` (safe integer), `packages/phase-f/lo3/cage.ts` (trusted mounts); plus Lo2, tick, evidence attestation and regression tests. No broad E2E pass inferred.

## Matrix / original spec coverage

- Constructed **509** spec-anchored *comparison and inventory* rows, across 21 categories (scope, 26 defaults, status/state/errors, DTOs, 12 canonical routes, FSM, timeout/incident, 12 screens, 14 components, UX, storage, auth, DOC-E evidence and broader design).
- Generated separate original-text ledger for **all 12,537** paragraphs including empty paragraphs, maintaining exact paragraph numbers; code manifest union **889** paths with old/current Git blob SHAs; 21-file delta manifest.
- Both snapshots statically match 26 cited config literal defaults, 12 named canonical API route wrappers, 12 page source paths, 14 named component paths, 4 status values, 8 FSM state values and 29 error-code literals. These are **presence/default equality**, NOT behavior or complete contract acceptance.
- At least some matrix rows anchor to broad original clauses; the 509-row register has NOT been demonstrated to be a complete atomic requirement denominator. **Overall DOC-C implementation/conformance % for both versions: NOT_COMPUTABLE**. Do not transform file presence, 509-row inventory, or historical 143 accepted items into a global %.
- Matrix has 412 entries with all candidate paths found in either snapshot; 1 DOC-E entry has no direct mapped source path and 3 other systems have no direct mapping. Other rows are enums, scope or microtests. These counts must NOT be used as pass rates.

## Independently run matched isolated tests

A six-case Node22 isolated source test suite used the ZIP files for old, and new code reconstructed from GitHub textual commit patch and verified against current exact Git blob SHA. Equal six cases:
1. canonical nested key deterministic ordering: old PASS / current PASS.
2. sparse array reject: old FAIL / current PASS.
3. Date prototype reject: old FAIL / current PASS.
4. cyclic input reject with demanded error type: old FAIL / current PASS.
5. unsafe max retry attempts reject: old FAIL / current PASS.
6. unsafe persisted retry counter reject: old FAIL / current PASS.

Old **1/6 = 16.67%**; current **6/6 = 100%** of these **six selected cases only**, never whole project. One extra current-only positive bounded retry test also passed (total current-only 7/7 but not fair version comparison).
Verified current blobs: `packages/core/canonical-json.ts` Git SHA `c0c14ca5a6fa16e2ebc9da191774d3306fc6c1ee`, `packages/queue/retry-policy.ts` Git SHA `9eb00e4cad9c5a284e64dccf8a8a2f4753f7882f`. Tests are not full repository Vitest/TypeScript/E2E/DB concurrency or security approval.

## Exact HEAD GitHub CI (independently retrieved)

Current HEAD `58b1200...` produced four completed failed GitHub Actions workflows:
- NEXY CI / Deploy Gate: https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37899764374
- Layer8 Cargo lock evidence: run 37899764452 (FAIL).
- Exact HEAD test evidence: run 37899764383 (FAIL).
- Six-system exact HEAD evidence: run 37899764371 (FAIL).
- Check-runs API: 15 checks, 12 FAIL + 3 SKIPPED, including production Deploy skipped. Actual logs for sampled failed jobs returned GitHub 404 BlobNotFound, so **failure root cause UNKNOWN**; do not infer code defect versus runner/infrastructure.

## Artifact SHA-256 (local comparison outputs)

- `NEXY_AI_spec_comparison_audit_20261010.xlsx`: `edaefb336300c6e72b374038d0695f88e8ddb8a1b18362d6a86592020ffb7de2`
- `NEXY_spec_all_12537_paragraphs.csv`: `8d28b52976eb9bcc73479268707010853f585d13da5a116a9e35a848fc12a45f`
- `NEXY_source_manifest_889.csv`: `6f09e8382ddf4e853d9dd25e06e38277794aa2033f51c5ac6a00a2b544e51cc1`
- `NEXY_feature_matrix.csv`: `2706569c743e8b473b3ac3ca419d5814db6d8de30bdfb1175f1427bed0ca3b44`
- `NEXY_delta_21_files.csv`: `c04356c59bee56611c1541c35999ba91832465ffea5a43ecb0c366cca511eb68`

These artifacts were created in the current chat working container. The remote AI-CONTEXT report records their cryptographic identity, but does not itself embed or upload the binary/CSV bytes. **No claim that full files exist in this repository.**

## Status

- Structural Git delta: VERIFIED.
- Original DOCX existence and hash: VERIFIED.
- 509-row inventory existence and 12,537-paragraph ledger: GENERATED and file-integrity checked; NOT full semantic audit.
- Selected local 6-case regression delta: VERIFIED WITH LIMITED SCOPE.
- Both versions' total specification compliance: UNKNOWN / NOT_COMPUTABLE.
- Current exact-head CI: FAIL reported; causal interpretation UNKNOWN.
- Production operational status/security signoff: NOT_VERIFIED.
- No Product branch, files, commits, workflows or settings mutated by this audit.
