# TEMP MEMORY — NEXY Lo4 Q64.64 Decision Utility Fabric

Status: IN_PROGRESS until GitHub write-back and re-read verification complete.
Chat reference: `CHAT-20261005-0230-NEXY-LO4-Q64-DECISION-UTILITY-FABRIC-SOL`
Date: 2026-10-05 (+07:00)
Storage target: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0230-NEXY-LO4-Q64-DECISION-UTILITY-FABRIC/`

## Objective
Design and implement 20 new Lo4 proposal systems using Q64.64 fixed-point arithmetic, with executable code, tests, evidence and explicit NEXY compatibility boundaries, without mutating any repository whose name contains `NEXY.AI`.

## Scope lock
IN SCOPE:
- AI-CONTEXT read/write.
- New additive folder under `คลังข้อมูลเสริม/` only.
- Read-only NEXY context from AI-CONTEXT.
- TypeScript/JavaScript fixed-point library and 20 Lo4 engines.
- Build/static/unit/stress verification.
- Integration contracts that keep Lo4 advisory until formal promotion.

PROTECTED / OUT OF SCOPE:
- Any mutation to a repository whose name contains `NEXY.AI`.
- Canon promotion.
- Deployment claims.
- Runtime integration claims against NEXY implementation.
- Secrets/credentials.

## Authority resolved
1. Current explicit user directive.
2. AI-CONTEXT Execution Kernel + global/security/verification rules.
3. NEXY context authority: DOC-B system law; DOC-C build authority; DOC-D only where supported; DOC-E deployment evidence.
4. Current implementation/runtime evidence when available.
5. Lo4 proposals in this folder.

## Key source facts used
- NEXY is a deterministic AI control/orchestration hub.
- External models/workers do not become final authority.
- Stable release direction is one legal verified output or freeze/silence.
- Current source normalization denominator is 837 normalized requirement rows; legacy 215 count is deprecated/unreliable.
- Lo4 in this task is proposal-only and may not promote itself into Canon.

## Implementation state
- Shared signed Q64.64 kernel implemented with `bigint`, exact scale `2^64`, signed 128-bit raw bounds.
- 20 orthogonal decision/utility engines implemented.
- NEXY Lo4 JSON-safe envelope implemented; Q64 raw values cross boundary as decimal strings.
- Public safe boundary converts validation/arithmetic exceptions into FREEZE.
- Deterministic canonical JSON serializer implemented.
- No external runtime dependency in compiled JS.

## Failure / repair history
1. Rust target attempted first. Runtime lacked `rustc`/`cargo`. Status: BLOCKED for Rust. Correction: TypeScript/BigInt selected because current NEXY build context includes TypeScript and Node is available.
2. First strict TypeScript compile failed on one generic and two frozen-array inference errors. Root cause fixed without weakening compiler strictness. Recompile: PASS.
3. First engine test run: 28 PASS / 3 FAIL because tests expected ideal decimal values from inputs such as 0.1 while exact Q64.64 parsing truncates non-binary decimal fractions. Correction: tests changed to binary-exact fractions for exact equality while retaining a dedicated test that proves 0.1 truncation semantics. Final tests: PASS.
4. Local `npm install --save-dev typescript@5.8.3` did not complete within the 120-second execution window. No dependency-install success is claimed. Correction: verification used available `npx --yes tsc 5.8.3`; compiled `dist/` is retained so E2 tests run directly with Node without package installation.
5. First evidence-metrics command queried the wrong registry export name and failed. Correction: inspected actual compiled exports, switched to `LO4_ENGINE_REGISTRY`, regenerated metrics. This did not affect implementation behavior.
6. `npx --yes esbuild --version` exceeded the 60-second execution window. No bundler PASS is claimed. Correction: retain complete compiled `dist/` in a deterministic archive and generate text source snapshots for inspection.

## Current verification
- TypeScript strict compile: PASS.
- Static determinism gates: PASS.
- Unit + negative + adapter + stress + whole-registry determinism tests: PASS (41/41 at latest checkpoint).
- GitHub durable write: NOT_VERIFIED.
- GitHub re-read: NOT_VERIFIED.

## Resume point
Generate final docs/evidence/manifest, rerun verification into raw logs, commit unique folder to AI-CONTEXT main by fast-forward only, then re-read committed files and verify protected scope remained untouched.
