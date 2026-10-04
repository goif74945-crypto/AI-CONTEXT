# Architecture

## Pipeline

`Seed Case -> Relation Mutator -> Derived Case -> Target Adapter -> Baseline/Derived Observations -> Oracle -> Structured RelationResult -> VerificationReport`

## Modules
- `model.py`: immutable public contracts and status types.
- `canonical.py`: deterministic canonical representation and SHA-256 identity.
- `relations.py`: built-in relation factories and structural projection.
- `engine.py`: execution coordinator with fail-closed exception capture.
- `report.py`: stable report serialization.
- `cli.py`: minimal offline fixture validation utility.

## Authority boundary
MVK does not decide NEXY policy. The target adapter produces normalized observations. A relation oracle only judges the relationship specified by that test contract.

## Determinism boundary
Canonical hashes are deterministic only for supported canonical values. Unknown objects and non-finite floats are rejected. The system intentionally refuses repr-based fallback because repr may encode nondeterministic memory/process state.

## State model
The core engine is stateless across a report except for the supplied adapter. Relation replay may expose adapter state drift, which is a feature of deterministic-replay testing.

## Error model
- Mutator failure -> `ERROR` relation result.
- Adapter exception -> `ERROR` relation result.
- Adapter returns wrong type -> `ERROR`.
- Oracle exception -> `ERROR`.
- Oracle invariant violation -> `FAIL`.
- Oracle invariant satisfied -> `PASS`.

No exception is silently converted to PASS.

## Concurrency
Version 0.1 executes relations sequentially. This avoids accidental state races in adapters and preserves reproducibility. Parallel relation execution is a future option only for explicitly pure/stateless adapters.

## Evolution law
Public Case/Observation semantics should be versioned. New relations may be added without changing target adapters. Breaking changes to hash semantics require an explicit hash-schema version.
