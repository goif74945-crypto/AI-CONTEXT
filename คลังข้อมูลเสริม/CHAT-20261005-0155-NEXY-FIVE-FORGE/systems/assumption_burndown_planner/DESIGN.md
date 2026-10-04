# Assumption Burn-down Planner — Design

STATUS: PROPOSED_BY_AI / STANDALONE PROTOTYPE

## Objective
Turn explicit ASSUMPTION/UNKNOWN objects into a minimal bounded validation plan before protected mutation.

## Inputs
Assumptions carry impact, uncertainty and whether they block mutation. Probes carry cost, risk and the assumptions they can resolve.

## Optimization goal
Within `max_cost` and `max_risk`, enumerate bounded probe subsets and choose the one that:
1. covers every blocking assumption;
2. maximizes weighted risk burn-down across all assumptions;
3. uses lower cost, then lower risk, then fewer probes as tie-breakers.

Weighted assumption risk = impact × uncertainty.

## Invariants
- uncovered blocking assumption => FREEZE;
- a probe never implies resolution unless its ID explicitly lists the assumption;
- deterministic exact subset search for up to 20 probes;
- beyond 20 probes the prototype freezes rather than pretending exhaustive optimality.

## Evidence target
E2 tests cover blocking coverage, budgets, optimal bounded selection and impossible-plan freeze.
