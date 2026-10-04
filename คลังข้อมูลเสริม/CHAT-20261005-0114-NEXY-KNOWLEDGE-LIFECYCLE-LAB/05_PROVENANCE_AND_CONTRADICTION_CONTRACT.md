# Provenance & Contradiction Contract
> Classification: AI-PROPOSED CONCEPT.

## Evidence record
High-value evidence should expose source_identity, source_type, retrieval_time, publication_or_observation_time when available, immutable locator/revision, extraction method, scope, authority class, and integrity hash when practical.

## Contradiction record
contradiction_id; claim_ids; evidence_ids; contradiction_type; discovered_at; severity; adjudication_status; resolution; resolver_evidence; downstream_impact.

## Types
TEMPORAL: both may be true at different times.
SCOPE: different environments or populations.
SEMANTIC: same words, different definitions.
AUTHORITY: sources disagree.
MEASUREMENT: observations differ.
LOGICAL: cannot both hold under identical scope and time.

## Adjudication order
1. Normalize identity.
2. Normalize time.
3. Normalize scope/environment.
4. Normalize terminology and units.
5. Compare authority and directness.
6. If unresolved, preserve the conflict explicitly.

## Invariant
Never resolve contradiction by confidence arithmetic alone when authority, time, scope, or semantics can explain it.
