# Failure Atomizer — Design Contract

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON

## Objective
Shrink a concrete reproducible failure into a small human- and machine-inspectable witness.

## Inputs
Finite item sequence and a deterministic boolean failure predicate.

## Outputs
Evaluation trace plus `BASELINE_NOT_FAILING`, `EMPTY_CAUSES_FAILURE`, or `MINIMIZED_1_MINIMAL`.

## Minimality law
`MINIMIZED_1_MINIMAL` means no single remaining item can be removed while preserving the supplied failure predicate. It explicitly does **not** mean global minimum cardinality.

## Failure behavior
Evaluation budget exhaustion raises an explicit error. A non-failing baseline is never diagnosed as a failure.

## NEXY boundary
Future debugging/evidence tooling may use the minimized witness to make freeze causes reproducible, while canonical root-cause adjudication remains outside this helper.

## Verification model
E1 compile; E2 focused and negative-path unit tests; E3-local composition through `integration/test_portfolio.py`. Production integration is NOT_VERIFIED.
