# Architecture

## Purpose
The package is a **procedural adversarial layer**. It tests whether an EPC recommendation was reached through sufficiently independent, contestable, reversible, causally valid and explanation-complete procedure.

It is deliberately not:
- a proposal generator;
- a Canon author;
- a Core/JUDGE state machine;
- an automatic promotion engine;
- the global KEEP/CUT entitlement ledger;
- a replacement for NEXY verification or LAW.

## Flow

```text
CourtCase + externally-authorized CourtPolicy
        |
        v
semantic canonicalization
        |
        v
20 independent procedural organs
        |
        v
FREEZE > BLOCK > DEFER > READY_FOR_EXTERNAL_JUDGE
        |
        v
NEXY External-Judge REVIEW_ONLY envelope
        |
        v
External JUDGE / existing Canon-LAW verification path
```

## Numeric carrier
Every policy score is `bigint` signed Q64.64. `1.0 = 1 << 64`. Unit metrics are bounded to `[0,1]`. Division by zero, result overflow and invalid unit values throw explicit errors. Temporary BigInt intermediates may exceed i128; only represented Q64.64 results must satisfy the signed i128 range, preventing false overflow for valid ratios.

## Determinism
- no `Math.random`;
- no `Date.now` / wall clock;
- no binary-float score math;
- evidence and participants canonicalized by stable semantic IDs;
- presentation metadata excluded from semantic projection;
- canonical serializer rejects JavaScript `number` values;
- causal order uses explicit bigint ordinals supplied as evidence, not runtime time.

## Failure precedence
`FREEZE` outranks `BLOCK`, which outranks `DEFER`. Only an all-PASS twenty-organ result becomes `READY_FOR_EXTERNAL_JUDGE`. Even that state is not release/promotion authority.
