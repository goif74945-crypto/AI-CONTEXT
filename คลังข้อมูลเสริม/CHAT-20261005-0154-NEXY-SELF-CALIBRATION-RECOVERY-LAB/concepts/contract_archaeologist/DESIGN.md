# Contract Archaeologist — Design Contract

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON

## Objective
Extract exact regularities from finite execution traces without converting observations into requirements.

## Inputs
Iterable of mapping events with string field names and finite scalar values for mined scalar patterns.

## Outputs
`MiningReport` containing deterministic patterns and a content fingerprint. Patterns include required fields, observed constants, finite observed enums, numeric ranges, and exact finite-trace implications.

## Immutable rule
Every emitted pattern carries authority `OBSERVED_PATTERN_NOT_REQUIREMENT`. No causality, necessity, or normative law is inferred.

## Failure behavior
Malformed rows/keys, invalid parameters, or non-finite floats raise explicit errors. Empty input returns `NO_DATA`.

## NEXY boundary
Future use could compare observed runtime behavior to NEXY-owned contracts as a discrepancy signal. The observation itself must never become a canonical requirement automatically.

## Verification model
E1 compile; E2 focused and negative-path unit tests; E3-local composition through `integration/test_portfolio.py`. Production integration is NOT_VERIFIED.
