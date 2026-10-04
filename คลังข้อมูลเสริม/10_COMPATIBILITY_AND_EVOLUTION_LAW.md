# Compatibility and Evolution Law
Status: PROPOSAL / AI-PROPOSED CONCEPT
Authority: ADVISORY ONLY

## Problem
Deterministic systems still break when schemas, languages, evidence formats, tool contracts or policies evolve. “Backward compatible” is too vague unless compatibility dimensions are explicit.

## Compatibility dimensions
Syntax
Semantics
Serialization
Error behavior
Ordering
Identity/hash
Authority
Capability
Performance budget
Evidence format
Replay behavior
Migration behavior

A change can be compatible in syntax and incompatible in authority or hash identity.

## Change classes
C0 DOCUMENTATION_ONLY
C1 ADDITIVE_NON_AUTHORITY
C2 ADDITIVE_AUTHORITY_RELEVANT
C3 BEHAVIORAL_COMPATIBLE_BY_CONTRACT
C4 MIGRATION_REQUIRED
C5 BREAKING
C6 CANONICAL_IDENTITY_BREAK
C7 UNKNOWN_IMPACT

UNKNOWN_IMPACT must not be auto-promoted.

## Semantic versioning is insufficient alone
Version numbers summarize intent. Compatibility must be proven against invariants and representative historical fixtures.

## Evolution packet
Every authority-relevant change should eventually be describable by:
- old contract identity
- new contract identity
- change class
- affected invariants
- affected producers
- affected consumers
- migration function
- rollback function or explicit irreversibility
- compatibility tests
- evidence invalidation set
- deprecation horizon
- stop conditions

## Deterministic migration
For canonical data:
migrate(old) -> new must be deterministic.
Where reverse migration is claimed:
reverse(migrate(x)) == x for all supported x, or the loss must be explicitly modeled.

## Hash/canonicalization warning
Changing whitespace normalization, ordering, serializer, numeric representation, Unicode normalization or omitted/default fields can alter canonical hashes even if user-visible semantics appear unchanged.

## NX relevance
FACT_PROJECT: NX v0.1 describes a compact deterministic surface and canonical SHA-256 sealed result. Therefore future NX evolution should treat canonical identity behavior as an explicit compatibility dimension.

## Test matrix
- old producer -> old consumer
- old producer -> new consumer
- new producer -> new consumer
- new producer -> old consumer when promised
- old evidence -> new verifier
- new evidence -> old verifier when promised
- migrated artifact -> canonical identity expectations
- rollback after partial migration
- mixed-version cluster/workflow if applicable

## Acceptance
No compatibility claim without named dimensions and evidence. “It still builds” proves only a narrow property.
