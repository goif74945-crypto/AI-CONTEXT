# EMCR — Empirical Model Calibration Router

**Status:** AI_PROPOSAL / NON_GOVERNING

## Objective
NEXY is designed to hot-swap models/providers. Static labels like “best model” become stale. EMCR routes by capability-specific observed outcomes while penalizing miscalibration, latency, and cost under explicit budgets.

## Separation from conformance/substitution work
Conformance asks whether a model satisfies a contract. EMCR asks which currently eligible model has the strongest empirical routing score for one capability and budget. A model must still pass all authoritative admission/conformance gates first.

## Inputs
Observations: model, capability, success/failure, reported confidence, latency, cost. Route request: capability, minimum sample count, maximum latency/cost, minimum reliability.

## Invariants
- no samples → no invented quality;
- below minimum samples → `PROBE` rather than ROUTE;
- hard budget constraints are applied before ranking;
- score uses observed reliability and calibration error, not provider reputation;
- deterministic tie-breaking;
- observations outside [0,1] confidence or negative latency/cost fail closed.

## Scoring reference
Laplace-smoothed reliability minus mean absolute calibration error minus bounded latency/cost penalties. This formula is only a reference policy and must not be promoted without eval evidence.

## Failure semantics
Malformed observations → `FREEZE`; insufficient evidence → `PROBE`; no budget-compliant candidate → `FREEZE`; eligible best candidate → `ROUTE`.
