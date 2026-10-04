# Validation and Adoption Gates

## Classification
This file defines how AI-proposed concepts in this namespace could be evaluated. It does not authorize implementation.

## Gate A — Authority
Identify governing DOC-B/DOC-C/DOC-E implications. Any conflict blocks promotion.

## Gate B — Problem evidence
Demonstrate the target failure mode exists or has credible future value. Avoid building elaborate machinery for imaginary problems.

## Gate C — Minimal model
Define the smallest schema/state machine capable of expressing the concept. Avoid hidden heuristics.

## Gate D — Failure semantics
Specify UNKNOWN, CONFLICT, stale inputs, partial graph coverage, unavailable source, concurrency and recovery behavior.

## Gate E — Security/privacy
Prove the concept does not leak secrets, broaden privilege, create unsafe persistence or make provenance forgeable.

## Gate F — Determinism
For control-path use, specify deterministic inputs, ordering, time handling and replay semantics.

## Gate G — Performance/cost
Measure storage, retrieval, invalidation fan-out, indexing and latency. “Useful” is not permission for unbounded context growth.

## Gate H — Migration
Define how existing AI-CONTEXT records map into the new model without rewriting history.

## Gate I — Test strategy
Unit: schema/state transitions.
Contract: cross-component semantics.
Property: invalidation/replay invariants.
Integration: repository/evidence bindings.
Adversarial: stale evidence, forged provenance, cycles, conflicts.
Regression: known failure fossils.
E2E where user-facing behavior changes.

## Gate J — Shadow deployment
Run read-only alongside existing process. Compare findings without granting authority.

## Gate K — Promotion decision
Human/authorized system explicitly promotes or rejects. Record rationale and rollback.

## Required invariants
- proposal never masquerades as current implementation;
- stale proof cannot satisfy fresh obligation;
- UNKNOWN cannot silently become PASS;
- historical record is preserved;
- invalidation is scoped;
- no proposal can override higher authority.
