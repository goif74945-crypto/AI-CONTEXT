# Migration, Rollback, and Compatibility Contracts
Status: AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT

Every material migration should declare source_state, target_state, preconditions, transformation, invariants, irreversible_steps, checkpoints, verification, rollback_strategy, retention, and timeout/failure state.

Compatibility is a vector across schema, API, behavior, policy, authorization, storage, ordering, model/provider behavior, UI contract and observability. It is not a BOOLEAN.

Rollback classes: R0 stateless/config revert; R1 deterministic inverse; R2 compensating action; R3 snapshot/backup restore; R4 irreversible with explicit approval and forward recovery only.

A Git revert alone does not prove rollback safety. Data, external side effects, queued work, sessions, caches, policy state and provider actions must be covered.

Dual-read/dual-write requires an authoritative writer, reconciliation law, divergence detection, termination criteria and rollback semantics.

FREEZE when rollback anchor is absent, irreversible action lacks approval, migration provenance is incomplete, critical compatibility is UNKNOWN, or required proof cannot be regenerated.
