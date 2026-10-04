# Future Integration Proposal Only

> **AI PROPOSAL ONLY. NOT NEXY.AI AUTHORITY. NOT EXECUTED.**

This file proposes a safe adoption path if a future user explicitly authorizes integration into NEXY.AI. It does not grant such authority.

## Proposed Phase 0: refresh authority and state

1. Read current DOC-B/DOC-C authority.
2. Resolve exact target NEXY commit and branch.
3. Re-read all current TypeScript/Rust contract owners.
4. Diff them against this project's observed fixture.
5. If the sources disagree, record a conflict instead of choosing one automatically.

## Proposed Phase 1: read-only conformance

Do not generate into NEXY source yet.

- export a runtime/source snapshot from each current implementation;
- transform only explicit, authorized semantics into the forge snapshot shape;
- run `audit` in CI or locally as a non-mutating check;
- collect drift evidence.

Success criterion: the forge can detect intentional seeded drift and has no false positive on the exact approved contract.

## Proposed Phase 2: authority nomination

Choose a **small** contract where generation provides clear value. Explicitly decide:

- which document owns semantics;
- whether the neutral manifest is canonical or merely derived;
- which fields may be generated;
- which runtime-specific behaviors remain hand-authored;
- versioning and migration law;
- generated-file ownership labels.

Do not attempt a whole-repository conversion.

## Proposed Phase 3: generated shadow artifacts

Generate artifacts outside live import paths and compare against hand-written owners. Require:

- TypeScript strict compile;
- Rust `cargo check` under the exact NEXY toolchain;
- existing NEXY contract tests;
- conformance fixtures consumed by both runtimes;
- deterministic regeneration with a clean diff.

No behavior change is allowed in this phase.

## Proposed Phase 4: controlled adoption

Only after explicit authorization:

- replace one nominated duplicated data table with generated output;
- preserve hand-written runtime logic where the IR cannot express it;
- add a generated-artifact freshness gate;
- run full relevant NEXY regression suites at the exact commit.

Rollback is deletion/reversion of the generated integration commit while preserving the manifest/evidence for analysis.

## Proposed future IR extensions

These are ideas, not commitments:

1. recoverability/error catalogs;
2. numeric bounded fields and wire encodings;
3. request/response object schemas;
4. versioned compatibility transforms;
5. invariant DSL with code-generated conformance vectors;
6. proof metadata linking every generated member to source requirement IDs;
7. Rust/TypeScript parser generators for binary wire formats;
8. migration checks proving backward-compatible changes;
9. codegen provenance headers containing semantic fingerprint and source commit;
10. runtime attestation that reports the compiled contract fingerprint.

Each extension should first receive a formal requirement, failure model, and evidence plan. More machinery is not automatically more correctness. Humanity has already tested that hypothesis extensively.
