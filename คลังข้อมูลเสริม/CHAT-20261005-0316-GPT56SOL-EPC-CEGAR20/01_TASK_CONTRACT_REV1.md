# TASK CONTRACT REVISION 1 — TOOLCHAIN ADAPTATION

SUPERSEDES EXECUTION-TOOLCHAIN PORTION OF: 01_TASK_CONTRACT.md
DOES NOT CHANGE: objective, 20-mechanism surface, authority law, protected scope, vote law, Q64.64 requirement, acceptance semantics.

## Triggering evidence
Local isolated execution attempted Rust first.
Observed: `rustc: command not found`.
Available verified toolchain:
- Node.js v22.16.0
- TypeScript 5.8.3

## Smallest safe correction
Implementation language changes from planned Rust to standalone TypeScript ESM using BigInt-backed signed-i128 Q64.64.

This is compatibility-aligned with the inspected NEXY read-only surface:
- `packages/phase-f/lo3/governor.ts` uses bigint Q64.64.
It does NOT claim implementation integration.

## Revised verification gates
- E1: `tsc -p tsconfig.json` must PASS.
- E2: `node --test tests/*.test.mjs` must PASS on final bytes.
- E2 property/negative: deterministic grid/property suite must PASS.
- static policy scan: no Math.random, Date.now/new Date, fetch/http/network, eval/Function, f32/f64 authoritative path.
- deterministic replay/capsule: repeated identical input must be byte-identical.
- exact tested source/test/evidence SHA-256 manifest required.
- GitHub readback required after publication.

## Provenance
AI_CONTEXT_HEAD_OBSERVED_AT_REVISION: eb3b42e7c77ac44101cb9b9f24e8667e7a7df2fd
NEXY_PIN_READ_ONLY: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Rust-toolchain absence is an execution-environment limitation, not a change to NEXY requirements.
