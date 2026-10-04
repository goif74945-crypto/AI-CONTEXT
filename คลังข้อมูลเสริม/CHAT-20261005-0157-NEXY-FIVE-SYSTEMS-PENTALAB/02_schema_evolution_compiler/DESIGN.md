# Design — NEXY Contract Schema Evolution Compiler (CSEC)

**Status:** AI-PROPOSED / NON-AUTHORITY / NOT PRODUCTION INTEGRATED.

## Objective
Make compatibility/evolution claims executable and fail-closed.

## Algorithm
Canonicalize old/new simple contracts; require explicit one-to-one renames; compare type relation, requiredness, enum constraints, added/removed fields and additional-properties policy; classify BREAKING / MIGRATION_REQUIRED / ADDITIVE_COMPATIBLE / NO_STRUCTURAL_CHANGE; emit semver recommendation, migration steps, reason codes and fingerprint.

## Invariants
No inferred rename; many-to-one rename rejects; required additions without defaults break; enum narrowing breaks; field order does not affect fingerprint.

## Complexity
O(F log F) dominated by canonical sorting.

## Future NEXY boundary
Candidate for contract/tool/evidence-envelope migration preflight. Complements, not replaces, NEXY compatibility authority.

## Limits
Reference model is shallow and does not yet implement nested JSON Schema, protobuf wire rules, DB migration execution or consumer telemetry.

## Security boundary
No network access, credential handling, repository mutation, production side effect, or NEXY law override occurs in the reference engine. A future adapter must validate provenance and authorization.
