# Future Research Backlog

Every item below is **AI_PROPOSED**, not current NEXY scope.

## P1 — Cross-language conformance ports
Implement minimal TypeScript and Rust evaluators against `GOLDEN_VECTORS.json`. Gate adoption on exact vector parity and independently derived conversion tests.

## P2 — Signed-128 fixed-point contract compiler
Given an authorized numeric contract, determine the smallest safe decimal/rational quantum that preserves all explicit thresholds exactly while staying inside signed-128 range for declared bounds. Reject if no legal quantum exists.

## P3 — Interval propagation
Extend from an input interval to exact interval arithmetic across explicitly authorized arithmetic operations. Division across zero and nonlinear operations must freeze unless semantics are defined.

## P4 — Significant-figure semantics
Many measurements encode precision through significant figures rather than explicit `uncertainty_abs`. Design a separate contract rather than inferring significance from formatting.

## P5 — Provenance-bearing external rates
Currency or time-varying conversion requires signed source identity, observation time, validity window, freshness law, and proof invalidation. Never add a live-rate lookup as a hidden unit alias.

## P6 — Unit registry attestation
Version registries as immutable artifacts with reviewable diffs, hash identity, deprecation law, and compatibility tests.

## P7 — Decimal/fixed128 code generation
Generate host-language constants and parsers from an approved registry/contract without runtime dynamic evaluation.

## P8 — Numeric mutation testing
Mutate operators (`<`/`<=`), thresholds, scale factors, offsets, and rounding modes to measure whether a consuming test suite detects semantic corruption.

## P9 — Resource-envelope proof
Benchmark worst-case accepted rational sizes and derive explicit CPU/memory envelopes per operation rather than relying only on coarse input limits.

## P10 — Formal model
Model ACCEPT/REJECT/FREEZE interval classification and fixed128 projection in a theorem prover or model checker, then link machine-checked properties to golden vectors.
