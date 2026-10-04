# Deterministic Replay Specification

## Goal
Make any authoritative NEXY decision reproducible from a closed replay bundle.

## Replay identity
A replay is identified by:
- canonical input hash
- constraint/law set hash
- executable/build hash
- dependency lock hash
- configuration hash
- initial authoritative state hash
- evidence-set manifest hash
- agent topology/version manifest hash
- deterministic seed set, if any bounded pseudorandom mechanism exists
- expected terminal state
- expected authoritative output hash or explicit no-output class

## Replay bundle
A valid bundle SHOULD contain:
1. MANIFEST
2. INPUT
3. LAW_SNAPSHOT
4. STATE_BEFORE
5. EVIDENCE_MANIFEST
6. EXECUTION_TRACE
7. STATE_AFTER
8. OUTPUT_OR_FREEZE
9. VERIFICATION_REPORT

## Core properties
R1 Idempotent canonicalization.
R2 Same replay tuple produces identical terminal state.
R3 Same accepted replay produces identical output bytes/hash.
R4 A frozen replay cannot expose an authoritative output.
R5 Any mutation of a bound component changes replay identity.
R6 Replay verification never relies on wall-clock ordering unless time is an explicit signed input.
R7 Missing replay component is a verification failure, not a wildcard.

## Differential replay
Run the same bundle across supported environments. Compare:
- state transition sequence
- reason codes
- evidence cardinality
- consensus decision
- output hash
- freeze/recovery behavior

Any difference must be classified as: expected projection-only difference, non-authoritative telemetry difference, or authoritative divergence. Authoritative divergence is release-blocking.

## Metamorphic replay
Generate input transformations that should preserve meaning, then verify canonical identity or explicitly expected rejection. Examples: whitespace variants, stable field ordering, redundant transport framing, equivalent numeric serialization where the contract permits it.

## Negative replay
Corrupt exactly one component per case: evidence hash, law hash, state hash, build hash, signature, quorum record, transition event. Expected result is deterministic rejection/freeze with no accidental acceptance.

## Evidence
A replay report must record commands/tool versions actually executed. Planned commands are not evidence.
