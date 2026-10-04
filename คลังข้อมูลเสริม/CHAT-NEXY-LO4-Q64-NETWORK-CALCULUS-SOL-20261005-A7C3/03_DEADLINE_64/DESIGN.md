# DEADLINE-64 Design

**Status:** Lo4 AI proposal only.

## Objective
Certify a conservative upper delay for the same explicit arrival/service model and compare it with a deadline.

## Law
For a stable flow, use `D=T+b/R`. The fixed-point division `b/R` uses ceiling rounding so a non-representable fraction cannot understate the bound.

## Failure behavior
Unstable flow or malformed service returns `FREEZE`; an explicit deadline below the computed bound returns `FAIL`.
