# Proposed NEXY Integration Contract

Status: `EXPERIMENTAL PROPOSAL`, not current NEXY build scope.

## Boundary rules
- NEXY owns invocation authority and all state mutation.
- Engines receive immutable snapshots and return immutable advisory results.
- Inputs should be serialized through a versioned JSON contract before cross-language use.
- Adapter MUST reject unknown contract versions.
- Adapter MUST preserve deterministic ordering/canonicalization.
- Engine failure MUST become an explicit analytical failure/freeze signal, never an implicit approval.

## Suggested future placements
- Minimal-cut engine: requirement/evidence dependency analysis before release approval.
- Liveness sentinel: orchestration/task scheduler watchdog.
- Dominator analyzer: architecture/reliability planning and blast-radius analysis.
- Symmetry reducer: model-checking, simulation and test-corpus compaction.
- Lo4 tournament: experimental proposal laboratory only, upstream of any human/formal promotion gate.

## Promotion gate
A future promotion requires at minimum: canonical owner approval, port/equivalence proof, integration tests against exact NEXY revision, adversarial/resource tests, observability, rollback strategy and an explicit change to governing scope. This repository cannot grant that promotion itself.
