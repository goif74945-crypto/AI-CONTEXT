# Calibration Observatory — Design Contract

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON

## Objective
Measure whether stated confidence probabilities correspond to later verified outcomes.

## Inputs
Unique prediction records with probability in `[0,1]`, verified boolean outcome, and evidence-class label.

## Outputs
Brier score, fixed-bin expected calibration error, signed calibration bias, bucket details, and an advisory status.

## Interpretation law
Calibration is population evidence about confidence quality, never evidence that any individual decision is correct.

## Failure behavior
No data and insufficient sample size are explicit. Duplicate IDs, invalid probabilities, and invalid parameters are rejected.

## NEXY boundary
Future NEXY diagnostics may use this to detect chronic over/underconfidence in workers, judges, routes, or domains. It must not be used as a bypass around exact verification.

## Verification model
E1 compile; E2 focused and negative-path unit tests; E3-local composition through `integration/test_portfolio.py`. Production integration is NOT_VERIFIED.
