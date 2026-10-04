# Unknown Closure Planner — Design

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## Problem
Agents either guess missing information or over-question users. Both are bad: one risks correctness, the other wastes attention.

## Objective
Given requirements blocked by unknown facts and available probes/questions, compute the exact minimum-cost probe subset that resolves every currently blocking unknown.

## Algorithm
Exact subset search (bounded to 20 probes) with deterministic score:
`total cost → subset size → lexicographic probe IDs`.

This intentionally chooses certainty and reproducibility over heuristic approximation for the bounded planning surface.

## Outputs
- `PROCEED` when all blockers are already known;
- `ASK` with minimum probe/question set;
- `FREEZE` when at least one blocking unknown has no legal resolver.

## Invariants
- never guess an unknown;
- a plan cannot proceed with uncovered blockers;
- reordering probes does not change the result.

## NEXY value
Reduces unnecessary clarifying questions while keeping zero-guess behavior intact.
