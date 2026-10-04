# Decision Calculus for Autonomous Engineering

## Purpose
Choose among technically valid actions without sacrificing hard requirements for convenience.

## Candidate dimensions
objective contribution; requirement coverage; invariant risk; blast radius; reversibility; evidence strength; dependency uncertainty; operational cost; migration cost; future option value.

Never collapse these into one score before hard constraints are applied.

## Gate order
1. Authority: action is authorized.
2. Requirements: immutable requirements remain satisfied.
3. Integrity: protected state/secrets cannot be corrupted.
4. Evidence: critical premises are established.
5. Compatibility: consumers and contracts are mapped.
6. Reversibility: rollback cost/class is understood.
7. Utility: only surviving candidates compete on value.

Failure of gates 1–3 rejects a candidate rather than merely lowering its score.

## Pareto discipline
A dominates B only when A is no worse on every mandatory dimension and better on at least one relevant dimension. Preserve multiple candidates when trade-offs are real.

## Evidence-adjusted utility
Conceptually: expected value = benefit × evidence strength − failure cost × uncertainty exposure.
This is a reasoning aid, not measured truth unless its inputs are measured.

## Decision record
Persist objective, candidates, rejected alternatives, assumptions, unknowns, affected invariants, rollback path, post-action evidence and invalidation triggers.

## Re-open a decision when
requirements change; dependency contracts change; runtime evidence contradicts a premise; rollback becomes impossible; observed cost exceeds tolerance; or a critical UNKNOWN becomes known.

## Anti-patterns
Choosing easiest first; sunk-cost preservation; model-confidence-as-proof; local optimization that raises global recovery cost; scalar scores hiding constraint violations.
