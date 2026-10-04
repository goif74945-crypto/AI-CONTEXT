# DCPX — Diversity-Constrained Portfolio Composer

**Status:** `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING`

## Problem
Picking the individually strongest proposal can produce a brittle, redundant or unaffordable innovation program. DCPX chooses a portfolio, not a winner.

## Candidate fields
- conservative Q64.64 value;
- non-negative Q64.64 implementation cost;
- non-negative Q64.64 complexity tax;
- one or more domains;
- required candidate/capability IDs;
- explicit conflicts.

## Policy
- total implementation budget;
- total complexity budget;
- max selected count;
- minimum number of distinct domains;
- Q64.64 pair-overlap penalty weight.

## Exact reference algorithm
For at most 18 candidates, enumerate all subsets from size 1 through `max_items`. A subset is feasible only when dependencies, conflicts, cost, complexity and diversity constraints pass.

Score:

`sum(conservative_value) - sum(pair_penalty_weight * overlap(a,b) * min(value(a), value(b)))`

Tie break:
1. higher score;
2. lower total cost;
3. lower total complexity;
4. lexicographically smaller selected-ID tuple.

## Fail-closed rules
- all candidate pairs require overlap evidence;
- unknown dependency/conflict IDs freeze;
- >18 candidates freezes the reference engine rather than pretending exhaustive optimality;
- no feasible subset returns HOLD.

## Non-goals
This is a small exact reference solver, not a scalable production optimizer.
