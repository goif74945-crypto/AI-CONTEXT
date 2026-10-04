# Failure and Threat Model

## AURORA
- **Failure:** reward abstention so strongly that agents freeze on answerable tasks.
  - Mitigation: separate needless-abstention metric from unsafe-answer metric; policy can reject poor utility.
- **Failure:** confidence spoofing.
  - Mitigation: Brier calibration is diagnostic only; ground-truth/eval provenance must be trusted by the caller.
- **Failure:** biased eval corpus.
  - Status: external risk; not solved by this prototype.

## MARGIN
- **Failure:** wrong scale produces meaningless normalized margin.
  - Mitigation: explicit positive scale; scale ownership must come from policy authority.
- **Failure:** floating precision differences in TypeScript near boundaries.
  - Mitigation: Python reference uses Decimal; production TypeScript should use domain-appropriate fixed-point/decimal types for critical financial/safety thresholds.
- **Failure:** nominal threshold itself is wrong.
  - Status: policy-authority problem, not solvable by arithmetic.

## UPA
- **Failure:** callers coerce UNKNOWN/CONFLICT to truthy/falsey values.
  - Mitigation: explicit enum/class and `releaseable` only for TRUE.
- **Failure:** misuse of `knowledgeJoin` to merge evidence that is not independent.
  - Mitigation: caller must bind provenance and independence policy.

## TRACEWEIGHT
- **Failure:** fake graph claims independent ancestry.
  - Mitigation: graph provenance must be generated from actual orchestration traces in a future integration.
- **Failure:** cyclic derivation.
  - Mitigation: explicit cycle detection and failure.
- **Failure:** equal weights are asserted without basis.
  - Mitigation: weight ownership must be explicit and testable.

## CONTRACT-DRIFT
- **Failure:** semantically equivalent strings look different or semantically different strings look equal.
  - Mitigation: prototype operates on normalized structured contract atoms; semantic normalization belongs upstream.
- **Failure:** caller marks a dangerous event approved without real authority.
  - Mitigation: future integration must bind approval tokens to User Law / authorized principal evidence.

## Shared abuse cases
- NaN/infinite/non-positive numeric inputs: rejected where relevant.
- duplicate identifiers: rejected.
- missing graph parents: rejected.
- graph cycles: rejected.
- empty proof sets where a proof is required: rejected.
- silent contract expansion / invariant removal / evidence weakening: freeze by default.
