# C2 — Context Noninterference Sentinel (CNS)

Status: `AI_PROPOSED_CONCEPT`

## Objective
Test a finite noninterference property: fields declared excluded/irrelevant/untrusted must not change a deterministic decision across the supplied mutation set.

## Inputs
- baseline context;
- mutation sets keyed by excluded field;
- deterministic decision function;
- optional joint-mutation budget.

## Invariants
1. Baseline decision is fingerprinted canonically.
2. Each declared mutation is evaluated against the same baseline context.
3. Optional Cartesian joint mutations detect interactions between excluded fields.
4. A decision change or evaluation exception is a failure, never silently ignored.
5. Cartesian explosion is explicitly bounded; exceeding budget blocks rather than truncating evidence silently.

## Output
- `PASS` only when every executed mutation yields the baseline decision fingerprint;
- `FAIL` on influence/evaluator failure;
- `BLOCKED` on invalid configuration or mutation budget exhaustion.

## Evidence semantics
PASS means only: “within this finite declared mutation campaign, excluded context did not alter the decision.” It is not a universal theorem.

## NEXY value
Provides behavioral evidence that context routing/privacy/taint boundaries are not merely configured but actually non-influential for tested decision paths.
