# Design — Acceptance Mutation Sentinel (AMS)

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Objective
Measure whether an acceptance/release gate is strong enough to reject deliberately corrupted variants of an otherwise valid result.

## NEXY value
A test can pass while proving almost nothing. AMS attacks the gate itself. If deleting evidence, flipping PASS to FAIL, or removing verification still satisfies the gate, the gate is weak even though the happy path is green.

## Core contract
- A valid baseline must be accepted first; otherwise `INVALID_BASELINE`.
- Every mutator receives a deep copy of the baseline.
- A mutation is **killed** when the gate rejects it.
- A mutation **survives** when the gate still accepts it.
- `kill_rate = killed / total`.
- no mutators -> `NOT_VERIFIED`.
- mutation execution errors -> `MUTATOR_ERROR`.
- any survivor -> `WEAK_GATE`.
- all mutations killed -> `PASS` for the supplied mutation set only.

## Failure semantics
PASS does not prove the gate is universally complete; it proves only that it rejected the enumerated mutation operators. Mutation-set coverage must therefore be evidence-scoped.

## Complexity
O(M*G), where M is mutation count and G is gate-evaluation cost.
