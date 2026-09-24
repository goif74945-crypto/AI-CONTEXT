# FSM Registry Validation

## Result
**PASS — FSM namespace / structural validation**

- source-defined ontology FSMs: **8**
- source FSMs represented: **8**
- implementation-observed-only state models: **1**
- total registry records: **9**
- duplicate FSM IDs: PASS
- duplicate namespaces: PASS
- source FSM coverage: PASS

## Namespace law
State labels are not globally unique concepts.

Examples:
- `ACTIVE` in App Lifecycle ≠ `ACTIVE` in Capability Registry ≠ `ACTIVE` in Global Constitutional FSM.
- `RUNNING` in DOC-C Execution ≠ Queue Job `RUNNING` ≠ implementation PipelineRun `RUNNING`.
- `FREEZE` / `FROZEN` / `FAILSAFE` are not automatically aliases.

Every transition must be interpreted inside its `namespace`.

## Implementation-observed distinction
`IMPL-FSM-PIPELINE-RUN` is deliberately registered as implementation-only because `packages/queue/run-state.ts` explicitly describes a per-run state model separate from the global FSM.

It must not be promoted to source canon automatically.

## Known review items
- Capability source FSM includes `QUORUM_SIGNED` and `ACTIVE`; observed Phase-F implementation exposes `PROPOSED | REVIEWED | ANCHORED | DEPRECATED` and quorum evaluation separately.
- Queue Job source FSM is not identical to BullMQ internal state representation.
- Risk/Intelligence source gives the five-state model; observed Rust kernel supplies a concrete transition table and monotonic failure mapping.
