# Survivability and Degraded-Mode Design
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

## Principle
Availability is not success if the system remains online by inventing truth. A degraded system must expose exactly which guarantees remain valid.

## Capability lattice
Instead of UP/DOWN, model capabilities independently:
READ_VERIFIED
READ_STALE_BOUNDED
WRITE_REVERSIBLE
WRITE_IRREVERSIBLE
AUTHORITY_RESOLUTION
EVIDENCE_GENERATION
EVIDENCE_VERIFICATION
EXTERNAL_FETCH
LOCAL_COMPUTE
CANONICAL_EMIT

A failure removes capabilities. It must not silently weaken their contracts.

## Degraded states
D0 NORMAL
D1 READ_ONLY_VERIFIED
D2 READ_ONLY_BOUNDED_STALE
D3 COMPUTE_NO_AUTHORITY
D4 AUTHORITY_NO_EXECUTION
D5 EVIDENCE_UNAVAILABLE
D6 ISOLATED_RECOVERY
D7 FREEZE

## Safe degradation examples
- external fetch unavailable: use only explicitly allowed cached evidence with proven identity/freshness contract
- mutation backend unavailable: preserve read-only analysis; do not queue ambiguous writes
- authority source unavailable: computation may continue for diagnostics but canonical emit freezes
- verifier unavailable: artifact may be produced as UNVERIFIED but cannot satisfy release claim

## Unsafe degradation
- replacing missing authoritative value with model guess
- returning last-known value without staleness metadata
- dropping a required validation gate
- widening tool permissions to recover availability
- changing deterministic error into best-effort success

## Recovery invariants
Recovery must prove:
- queued actions are still authorized
- source/spec did not change during outage
- idempotency/replay rules hold
- partial writes are detected
- stale caches are invalidated
- evidence generated during degraded mode is correctly classified

## Game-day scenarios
- time authority disappears
- evidence store is readable but not writable
- verifier version mismatch
- network partition between decision and execution
- duplicate delivery after retry
- rollback target lacks compatible schema
- dependency returns conflicting data after recovery

## Acceptance
For each critical dependency, document:
dependency -> lost capabilities -> permitted actions -> forbidden actions -> recovery proof -> terminal FREEZE condition.
