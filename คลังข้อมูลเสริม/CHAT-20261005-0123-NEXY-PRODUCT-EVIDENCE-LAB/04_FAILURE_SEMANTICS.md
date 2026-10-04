# 04 — Failure Semantics

## Compile-time validation failure

Used when the proposed experiment is structurally invalid or prohibited. No contract is emitted.

Examples:
- missing population;
- impossible baseline/MDE combination;
- mean metric without planning standard deviation;
- empty guardrail set;
- prohibited risk flag such as `dark_pattern` or `privacy_violation`.

## `FREEZE`

Used after a contract exists but evidence cannot safely cross the evidence boundary.

Triggers in this prototype:
- contract hash mismatch;
- critical data-quality/invariant violation;
- hard guardrail degradation beyond the explicit threshold.

`FREEZE` is intentionally stronger than `INCONCLUSIVE`.

## `INCONCLUSIVE`

The evidence is not sufficient to classify the hypothesis threshold. Typical cases:
- sample size is below the planned per-arm minimum;
- the confidence interval overlaps the MDE threshold.

## `REJECTED`

With adequate sample size and no blocking guardrail, the confidence interval is wholly below the configured MDE threshold in the desired direction.

This means the tested evidence does not meet the predeclared product hypothesis threshold. It does **not** mean the feature is universally bad.

## `SUPPORTED`

With adequate sample size and no blocking guardrail, the confidence interval wholly clears the MDE threshold in the desired direction.

This is evidence support, not automatic shipping authority.
