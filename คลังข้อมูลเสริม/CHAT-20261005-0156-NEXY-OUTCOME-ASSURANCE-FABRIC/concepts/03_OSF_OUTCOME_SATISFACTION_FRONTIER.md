# OSF — Outcome Satisfaction Frontier

`AI-PROPOSED / EXPERIMENTAL`

## Problem
A single weighted score can erase meaningful tradeoffs: one candidate may be faster while another is more satisfying or robust.

## Behavior
OSF removes candidates that `FAIL` or `FREEZE`, then computes exact Pareto nondominance across soft-criterion margins.

## Key invariant
A candidate is dominated only if another is no worse on every soft dimension and strictly better on at least one.

## User value
NEXY can present a small set of genuinely distinct best tradeoffs without pretending user priorities are known when they are not.
