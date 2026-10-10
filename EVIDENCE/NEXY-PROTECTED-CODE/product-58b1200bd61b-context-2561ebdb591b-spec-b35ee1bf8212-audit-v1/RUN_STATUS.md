# NEXY exact-spec protected-code audit — SOURCE-VERIFIED PARTIAL CHECKPOINT

Event type: AUDIT_CHECKPOINT_NOT_PROTECTED
Product repository: goif74945-crypto/NEXY.AI-
Product branch: NEXY.ai (READ ONLY)
Pinned product HEAD: 58b1200bd61b867e917057d0019eea78ea9f6b2a
Product tree: 1092 entries (203 trees; 889 blobs), GitHub git/trees?recursive=1 truncated=false
Control repository/branch: goif74945-crypto/AI-CONTEXT / main
Spec file: แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20261008-072414).docx
Spec SHA-256 **computed from 2,146,350 raw DOCX bytes**: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7; 12,537 Document.paragraphs; 0 Document.tables; 17 sections. Original-name Project-file copy could not be raw-byte materialized; the dated copy did materialize and independently matches the expected hash. No inference from prior reports.
Authority: COMMANDS/20261010-GPT6-SOL-NEXY-EXACT-SPEC-CONFORMANT-CODE-AUDIT-AND-LOCK-V1.md, POLICIES/20261010-NEXY-VERIFIED-CODE-PROTECTION-V1.md, POLICIES/20261010-NEXY-EVIDENCE-GATED-CONTINUOUS-UPDATE-V1.md, AGENTS.md in product and control.
Authority order: owner + actual DOCX > product AGENTS.md/permissions > scoped NEXY policy > older atlas/history. 88 atlas groups and 143 old checks are NOT normative requirement denominators.

## Observed coverage, non-equivalence warning
- Git tree enumerated completely: 889 of 889 Git blobs / 203 trees; GitHub response truncated=false.
- Repo Code Bridge literal no-hit scan exact HEAD: candidate_files=889; inspected_files=889; searched_files=887; skipped_files=2; failed_files=0; coverage_complete=false; results_truncated=false; warnings=[SEARCH_CONTENT_SKIPPED]. Full-text skipped: package-lock.json (SIZE_LIMIT); packages/lo2/engine.ts (NON_UTF8_OR_SIZE_LIMIT). **Inspected does not mean file content fully read or semantics reviewed**.
- Direct full content fetched independently for 8 named source/test/config documents: AGENTS.md, package.json, packages/auth/otac.ts, packages/auth/device-binding.ts, packages/core/vnext-state-matrix.ts, apps/web/app/api/auth/request-otac/route.ts, apps/web/app/api/auth/verify-otac/route.ts, tests/contract/state-matrix.test.ts (exact Git blob SHA in SOURCE_READ_LEDGER.jsonl). Full semantic review / caller graph is NOT complete.
- DOCX paragraphs 9846–10999 include 1,149 nonblank paragraph candidates. This is an INITIAL LOCATOR COUNT, *not* a complete atomic normative requirement denominator. The full 12,537 paragraph local index was created but 1,149 clauses have not been atomized, acceptance-tested, or reviewed to completion.
- Source FULL_READ coverage: 8 / 889 known blobs directly fetched. Eligible text denominator and binary classification remain UNKNOWN. Semantically certified source files = 0; VERIFIED atomic spec clauses = 0; PROTECTED units = 0. Do not interpret this as code-compliance percentage 0%; compliance itself is UNKNOWN.
- DOC-E gates E1–E12 all NOT_VERIFIED_CURRENT_HEAD; E11 owner release signoff NOT_VERIFIED. 4 source-HEAD workflow runs on 2026-10-09 concluded failure; reason/code-vs-infra not established.
- Audit checkout unavailable: container has Node v22.16.0, npm 10.9.2, git and curl but github.com name resolution failed (`curl: (6) Could not resolve host: github.com`), and cargo is not installed. No product Vitest/typecheck/cargo/migrations/browser-E2E executed. Source-only isolated reproducer described below is NOT a product integration test.

## Negative witness — NOT PROTECTED
- Code path: packages/auth/otac.ts ; Git blob bb6134ab1946c8cfa8f130eb7eea5a777d02c58e ; symbols: safeEqual; computeDeviceId.
- Actual pinned source: https://github.com/goif74945-crypto/NEXY.AI-/blob/58b1200bd61b867e917057d0019eea78ea9f6b2a/packages/auth/otac.ts
- isolated Node 22.16.0 test reproducing exact expressions fetched from source (not running product source module), command: node --test ./otac-expression-reproducer.cjs; CWD /mnt/data/nexy-audit-58b1200b; exit 1; cases 5, PASS 2, FAIL 3.
- Witness #1: equal JS string length with unequal UTF-8 byte lengths (é/a and 🙂/ab) triggers exception instead of false from timingSafeEqual.
- Witness #2: (foo1, 2.3.4.5) and (foo, 12.3.4.5) concatenate identically, so computeDeviceId yields identical SHA-256 values.
- Reproducer artifact SHA-256 f9a7a163b5911dae309204b80f6b60e44a5111dd8cde6823d3e51f2e25f28e19.
- Actual isolated test log SHA-256 62611f662351d0f4c8c19108b343c02cbdc577726e7f26b45180b05ac5a4ab98.
- Exact reachability/production exploitability not demonstrated. Do not assert that production session binding (implemented separately in packages/auth/device-binding.ts) uses this vulnerable function. Negative witness is reproduced only for isolated transcribed expressions.

## CI at exact HEAD
- https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37899764374 — NEXY CI / Deploy Gate: failure
- https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37899764452 — Cargo lock evidence: failure
- https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37899764383 — Exact HEAD test evidence: failure
- https://github.com/goif74945-crypto/NEXY.AI-/actions/runs/37899764371 — Six-system exact HEAD evidence: failure
- Check runs include skipped downstream gates and failures; no authenticated assertion-level root cause established. Do not label software broken only from failed job conclusion.

## Protection gate
PROTECTED_UNITS = **0**.
For protection require: original spec anchor + atomic normative assertion + pinned path/blob/symbol + dependency/caller map + positive/negative/integration tests (real run) + independent adversarial review + current-head proof. None has full evidence for acceptance. No whole-file lock.
PROTECTION_POLICY_READ = TRUE. POLICY_INSTRUCTIONS_SAVED_PREVIOUSLY = TRUE (control AGENTS and policies at the pre-run control HEAD). NEW_PROTECTED_PROOF = FALSE.
GITHUB_ENFORCEMENT_CONFIGURED = FALSE (not configured by this audit; no actual server-side rule inferred). Product source files changed by this audit: ZERO.
Status: **NOT_100_PERCENT_VERIFIED**; this is a resumable partial audit, not a full audited or released system.

## Builder CHANGE_REQUEST guard
A builder proposing a protected-contract change must: read current active protection events; pinpoint the DOCX P-number or reproducible defect; refresh product HEAD and every impacted source/dependency blob; show minimal diff, affected unit, risk/rollback, owner-specific authorization, independent review and old/new positive/negative/integration/regression results; use the canonical branch only and CAS. A protected unit cannot be arbitrarily renamed/refactored. Missing proof -> FREEZE affected change, never fake PASS.
This audit prohibits product writes, workflow dispatch, branch changes and production deployment.