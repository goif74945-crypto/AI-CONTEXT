# NEXY Integration Contract — CISF20

## Compatibility evidence inspected

NEXY read-only target:

- repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

Observed implementation facts at that revision:

1. `core-kernel/src/engine/fixed128_math.rs` defines signed Q64.64 on an `i128` raw carrier and fail-closed arithmetic boundaries.
2. `packages/phase-f/lo3/governor.ts` explicitly states authoritative numeric scoring uses signed Q64.64 carried by `bigint`, with i128 range checks.
3. NEXY state ownership source/search evidence assigns `boot/execute` to CORE, `agents_done` to SWARM, `verified/accepted/rejected` to JUDGE, and `freeze/stop` to SYSTEM.
4. Existing Lo2 refinement contains experimental law-candidate/promotion-proof governance; CISF20 must not replace it.

## Adapter direction

Recommended future dataflow:

```text
Candidate / test evidence
        |
        v
External adapter normalizes bounded CISF20 Evaluation
        |
        v
CISF20 pure advisory analysis
        |
        v
Interaction certificate + explicit witnesses
        |
        v
Existing NEXY evidence/JUDGE-facing path
        |
        v
NEXY authority decides what the evidence means
```

CISF20 never owns the final arrow.

## Interface

Pure API:

```text
runCisf20(evaluation, { baseline? }) -> advisory analysis
```

Wire protocol:

```text
NEXY-EPC-CISF20/1
Q64 wire values = canonical signed decimal raw integers
```

CLI:

```bash
node tools/cisf20-cli.mjs input.json
```

## Forbidden integration patterns

Do not:

- map `compensationMirage=true` directly to a NEXY `rejected` transition;
- map a good certificate to `accepted`;
- call this package from a path that bypasses LAW/JUDGE verification;
- interpret `ICC64.analysisSha256` as a signature or trust root;
- let input choose arbitrary NEXY actor/state/transition fields;
- treat a standalone PASS as deployment evidence.

## Q64 compatibility note

This package's raw representation and TypeScript operations intentionally match the current Lo3 `bigint` surface for add/sub/mul/div. The NEXY Rust Fixed128 implementation uses its own exact wide-intermediate algorithms. CISF20 production analyzers multiply non-negative unit metrics/weights/deficits and derive signed coupling by subtraction, avoiding reliance on unverified cross-runtime negative-multiplication rounding equivalence.

If a Rust adapter later exposes generic signed multiplication behavior, add exact cross-runtime vectors before claiming byte-for-byte semantic equivalence.

## Integration verification still required

Before promotion/integration into NEXY:

- choose the authoritative adapter call site;
- map NEXY evidence objects to the CISF20 bounded matrix;
- run NEXY contract/integration/regression suites at the exact integration commit;
- confirm no authority bypass/module-boundary violation;
- add exact TS↔Rust Q64 vectors if signed operations cross the boundary;
- seal evidence under the NEXY release process.

INTEGRATION_STATUS: `DESIGNED / STANDALONE_EXECUTED / NEXY_INTEGRATION_NOT_PERFORMED`.

## Exact inspected blob identities

- Rust Q64 core: `e0e1d4b3fa47d40ac9b30ae14ea8b7ae0ac58313`
- Lo3 governor: `7270c90a1debbf9c3ce3aada2aef6222b322c58c`
- Lo2 refinement: `52bd8d38e998c3dd31380cd0f7a1b75ea8857bbd`
- TypeScript VNext matrix: `27e1281fba330784cc3bf2c30e9e1e82f951479b`
- Rust VNext matrix mirror: `c55e13839f2bed01a29749f226edef82d1929a4a`
- state-matrix tests: `62dacf510f746d617abc7ea7293d250436ced6e0`
