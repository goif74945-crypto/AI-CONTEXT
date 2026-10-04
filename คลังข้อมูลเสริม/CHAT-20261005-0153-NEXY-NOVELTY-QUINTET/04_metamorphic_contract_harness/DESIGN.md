# Design — Metamorphic Contract Harness (MCH)

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Objective
Test deterministic transformations even when there is no complete oracle describing the exact correct output for every possible input.

## NEXY value
Canonicalizers, normalizers, serializers, ranking preprocessors, and adapter transforms often have invariant properties that are easier to state than all expected outputs. Examples: idempotency, key-order invariance, reversible transforms, normalization stability.

## Core contract
A `Relation` contains:
- `name`
- `mutate(seed) -> transformed seed`
- `holds(function, original, mutated) -> bool`

The harness evaluates every seed × relation pair using deep copies, records mutation/relation exceptions explicitly, and never hides a failed check.

## Status law
- zero executed checks -> `NOT_VERIFIED`
- any violation/error -> `FAIL`
- all executed relations hold -> `PASS`

## Integration caution
A metamorphic relation is itself a requirement. Bad relations can prove nonsense. In future integration, relation definitions must be authority-bound and versioned like tests, not generated ad hoc and promoted to truth.

## Complexity
O(S*R*C), where S is seed count, R relation count, and C cost of the function/relation evaluation.
