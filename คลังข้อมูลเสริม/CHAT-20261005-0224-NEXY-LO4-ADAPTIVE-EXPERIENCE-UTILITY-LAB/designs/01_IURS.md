# IURS — Interval Utility Regret Selector

**Status:** `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING`

## Problem
Lo4 proposals frequently have uncertain expected benefit. Ranking a single optimistic point estimate rewards confidence theater. IURS requires an explicit lower/upper utility interval for every declared objective.

## Required input
- unique proposal IDs;
- identical explicit objective sets;
- Q64.64 utility intervals in `[0,1]`;
- Q64.64 objective weights summing exactly to one;
- optional protected conservative minima;
- maximum allowed worst-case regret.

## Algorithm
For each candidate:
- conservative utility = weighted sum of interval lower bounds;
- optimistic utility = weighted sum of interval upper bounds;
- protected objectives are checked on lower bounds;
- global ideal = maximum optimistic utility among candidates;
- candidate regret = global ideal - candidate conservative utility.

Choose the admissible candidate with minimum regret, then larger conservative utility, then lexical ID. If all candidates violate protected minima, `FREEZE`. If best regret exceeds policy, `HOLD`.

## Invariants
1. Protected minima cannot be compensated by unrelated gains.
2. Objective-set mismatch freezes.
3. Duplicate proposal IDs freeze.
4. Weights must sum exactly to Q64.64 one.
5. Same logical inputs produce the same fingerprint regardless of candidate order.

## Non-goals
IURS does not estimate utilities, fabricate confidence intervals, prove business value, or approve adoption.
