# Multidimensional Compatibility Matrix
Status: PROPOSAL

## Why
“Compatible” is meaningless unless dimensions are named. NEXY-like systems can be compatible at syntax level while incompatible in authority, evidence, determinism or runtime behavior.

## Dimensions
- schema/version
- parser/compiler
- runtime/toolchain
- operating environment
- protocol/API
- data model
- authority semantics
- failure semantics
- determinism guarantees
- evidence format/verifier
- security/capability policy
- migration/replay behavior

## Cell states
PROVEN_COMPATIBLE
PROVEN_INCOMPATIBLE
CONDITIONALLY_COMPATIBLE
NOT_TESTED
UNKNOWN
NOT_APPLICABLE

## Matrix record
Pair(A,B) + dimension + fixtures + environment + verifier + source identities + result + conditions + evidence pointer.

## Rules
M1 No global “compatible” from one green dimension.
M2 Backward compatibility and forward compatibility are separate.
M3 Parser acceptance is not semantic compatibility.
M4 Data migration success is not rollback compatibility.
M5 Same output with different failure semantics may be incompatible.
M6 Evidence format changes can invalidate release tooling even if product behavior is unchanged.
M7 Security-policy widening is a compatibility event and requires explicit review.
M8 Unknown cells stay unknown; do not infer by adjacency.

## High-value matrix views
- release N vs N-1
- toolchain current vs candidate
- evidence schema current vs verifier versions
- canonical language fixtures vs parser/compiler versions
- API producer vs consumer
- context schema vs old stored records

## Exit criterion for migration
Every REQUIRED dimension must be PROVEN_COMPATIBLE or have an authorized migration/exception. Aggregate percentage cannot override one critical incompatible cell.
