# Evidence Genealogy Engine — Design Contract

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON

## Objective
Detect when apparently separate evidence items are structurally correlated and therefore should not be counted as independent corroboration.

## Inputs
Evidence metadata for one claim: evidence ID, source root, method family, content fingerprint, revision.

## Outputs
Correlation components, explicit edges/reasons, stale evidence list, structural independent-group count, deterministic fingerprint.

## Independence law
Shared source root or identical content always creates a correlation edge. Method-family correlation is optional because independence semantics may vary by domain.

## Limitation
Group count is structural, not a probabilistic proof of statistical independence.

## NEXY boundary
Future NEXY proof aggregation can use this as a warning/gate before treating multiple artifacts as independent evidence. NEXY remains the authority deciding required evidence classes.

## Verification model
E1 compile; E2 focused and negative-path unit tests; E3-local composition through `integration/test_portfolio.py`. Production integration is NOT_VERIFIED.
