# Five AI-Proposed Future Ideas

**Classification:** EXPERIMENTAL / PROPOSAL, not NEXY law.

## 1. Failure Witness Distiller

Turn a giant failing request/context bundle into the smallest practical reproducer that still emits the *same exact* FREEZE/error signature. This reduces debugging entropy, improves incident handoff, and makes regression fixtures cheap enough to keep permanently.

Potential future extension: hierarchical chunk reduction for multi-file/state bundles, with provenance-preserving witness capsules.

## 2. Verification Portfolio Optimizer

Treat verification as a constrained portfolio problem: each claim has legal evidence classes, each check has cost and coverage, and the planner returns the cheapest legal set. This can reduce CI/runtime verification waste without weakening proof semantics.

Potential future extension: expected failure probability, cache freshness, parallel wall-clock scheduling, and risk-weighted objectives.

## 3. Boundary Payload Pathology Lab

Create a strict, deterministic pre-core boundary for serialized data. The prototype focuses on JSON ambiguities that routinely create cross-language security and determinism problems: duplicate keys, Unicode-normalization collisions, non-finite numbers, excessive nesting, oversized structures, and unstable key order.

Potential future extension: corpus generation across JSON/CBOR/MessagePack/provider adapters and cross-language canonical vectors.

## 4. Contract Mutation Adequacy Engine

Verification can be green while being useless. This engine deliberately damages a contract and asks whether the verifier notices. A low mutation score is evidence that tests/oracles are blind to important semantic changes.

Potential future extension: domain-aware operators generated from schema constraints, authority hierarchies, threshold semantics, and state-machine transitions.

## 5. Negative-Space Coverage Analyzer

Systems like NEXY are defined as much by what they must **not** do as by happy-path behavior. This analyzer makes that negative space measurable by requiring explicit deny/freeze/abuse evidence instead of crediting positive tests for prohibition coverage.

Potential future extension: direct adapter from the current normalized requirement matrix + test/evidence index to a release-blocking negative-space report.
