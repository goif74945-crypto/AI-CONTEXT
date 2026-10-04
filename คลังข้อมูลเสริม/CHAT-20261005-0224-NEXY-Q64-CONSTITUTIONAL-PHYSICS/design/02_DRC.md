# DRC — Decision Robustness Certificate Engine

## Objective
Answer a sharper question than “what decision did this score produce?”: **could any allowed input perturbation flip that decision?**

## Model
For linear score `S = bias + sum(weight_i * center_i)` and bounded feature perturbations `|delta_i| <= radius_i`, DRC computes:
- nominal score;
- exact conservative Q64 box radius `sum(abs(weight_i) * radius_i)`;
- lower and upper score bounds.

## Certificate law
- lower >= threshold -> `CERTIFY_ALLOW`;
- upper < threshold -> `CERTIFY_DENY`;
- otherwise -> `FREEZE / PERTURBATION_CAN_FLIP_DECISION`.

The asymmetry at equality is deliberate: threshold semantics are `score >= threshold` for allow.

## Invariants
Feature IDs are unique, radius is non-negative, canonical sorting makes result input-order invariant, and all arithmetic is checked Q64.64.

## Non-goals
No nonlinear certification, probabilistic distribution inference, causal inference, or policy authority. A future version could add interval/Jacobian/SMT backends behind the same certificate interface.
