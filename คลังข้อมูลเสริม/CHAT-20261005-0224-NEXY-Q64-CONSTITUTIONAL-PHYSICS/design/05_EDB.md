# EDB — Expectation Divergence Barrier

## Objective
Prevent an execution plan from being materially more harmful or different than the consequence preview used to communicate that plan.

## Inputs
Preview and executable consequence sets use exact consequence IDs. Each consequence has:
- impact in `[0,1]` Q64.64;
- positive importance weight Q64.64.

## Law
The two sets must contain the same IDs and the same importance model. EDB computes weighted absolute divergence and weighted harmful surprise. If weighted divergence exceeds the explicit tolerance, execution freezes.

## Hard mismatch rules
- empty preview -> FREEZE;
- executable-only consequence -> FREEZE;
- preview consequence absent from executable model -> FREEZE;
- importance changed between preview and execution -> FREEZE.

## Boundary versus consent systems
EDB does not decide whether the user granted permission. It asks whether the consequence model being executed is faithful to the consequence model that was exposed. Consent/authorization remains separate authority.
