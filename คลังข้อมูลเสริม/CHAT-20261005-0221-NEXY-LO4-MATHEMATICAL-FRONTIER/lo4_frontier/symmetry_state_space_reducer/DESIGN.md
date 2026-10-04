# Design — Symmetry State-Space Reducer (SSSR)

**Status:** Lo4 EXPERIMENTAL / no Canon authority.

## Objective
Collapse states that differ only by the identifiers/order of explicitly interchangeable entities, reducing redundant simulation/model-checking/test work.

## Contract
Input: mapping `entity_id -> {class, state}` where `state` is finite JSON-compatible non-relational state.
Output: SHA-256 canonical partition key.

## Canonicalization
Entity IDs are intentionally omitted. States are canonical-JSON encoded, grouped by class, sorted inside each class, and the class partitions are sorted before hashing.

## Invariants
- permutation inside a class preserves key;
- semantic state change changes canonical payload/key (subject to ordinary cryptographic hash assumptions);
- class boundary changes key;
- NaN/non-JSON data is rejected.

## Critical limitation
This v1 contract does not rename or canonicalize cross-entity references embedded inside state. Such relational state must use a future graph-canonicalization contract or must not be passed to v1.

## NEXY value
Can reduce combinatorial validation load where agents/resources are genuinely interchangeable, while preserving class distinctions such as worker vs judge.
