# Property & Eval Catalog

## Scope
Reusable properties for tests, model-based checking, fuzzing, simulation, and release gates.

## FSM properties
P-FSM-001 INIT cannot become RUNNING without READY.
P-FSM-002 STABLE requires the canonical acceptance path.
P-FSM-003 rejected consensus reaches FREEZE.
P-FSM-004 timeout in an owned active state reaches FREEZE.
P-FSM-005 FREEZE recovery requires recoverable reason + authorized actor.
P-FSM-006 recovery target is READY.
P-FSM-007 STOP is terminal unless an authoritative specification explicitly says otherwise.
P-FSM-008 unknown event never creates a new state.

## Release properties
P-REL-001 confidence below configured canonical threshold cannot release.
P-REL-002 deterministic match below threshold cannot release.
P-REL-003 quorum shortfall cannot release.
P-REL-004 evidence shortfall cannot release.
P-REL-005 stale release token cannot release after freeze/recovery.
P-REL-006 release evidence binds exact tested head/state.
P-REL-007 partial gate success is never interpreted as total acceptance.

## Evidence properties
P-EVD-001 duplicate evidence aliases count once.
P-EVD-002 unverifiable source does not silently become verified.
P-EVD-003 every authoritative claim has provenance.
P-EVD-004 provenance chain detects mutation.
P-EVD-005 evidence timestamp alone does not prove freshness of underlying content.
P-EVD-006 derived evidence identifies its parents.

## Determinism properties
P-DET-001 canonicalization is idempotent.
P-DET-002 deterministic functions have stable output for stable inputs.
P-DET-003 unordered collections are canonicalized before hashing.
P-DET-004 floating-point cannot enter an authority path where forbidden.
P-DET-005 locale/timezone/environment cannot alter authoritative semantics unless explicitly bound.

## Agent/swarm properties
P-SWM-001 unsigned proposal cannot count.
P-SWM-002 duplicate agent identity cannot inflate quorum.
P-SWM-003 agent crash cannot be interpreted as agreement.
P-SWM-004 verifier does not accept its own unverified assertion as evidence.
P-SWM-005 correlated agents are distinguishable from independent evidence sources.
P-SWM-006 context shard isolation failures are detectable.

## Security properties
P-SEC-001 user-controlled content cannot mutate law/config authority.
P-SEC-002 path traversal cannot escape bounded storage roots.
P-SEC-003 secrets never appear in durable public evidence.
P-SEC-004 authorization decision is bound to actor and action.
P-SEC-005 recovery cannot reuse pre-freeze authorization token.

## Test record schema
property_id, spec_source, fixture, pre_state, action, expected_state, expected_output_class, forbidden_observation, evidence, result, tool_version, commit/state hash, timestamp, reviewer.
