# Context Budget Optimizer — Design

STATUS: PROPOSED_BY_AI / STANDALONE PROTOTYPE

## Objective
Select the highest-value dependency-valid context subset within a token budget while never dropping mandatory records silently.

## Inputs
Context items: stable ID, token cost, relevance, authority, freshness, dependency IDs, mandatory flag.

## Invariants
- mandatory items and their dependency closure must fit or result is FREEZE;
- selected items always include all declared dependencies;
- unknown dependencies result in FREEZE;
- deterministic tie-breaking uses item IDs;
- no selected set exceeds budget.

## Algorithm
1. validate all values and dependency references;
2. compute mandatory dependency closure;
3. greedily evaluate each remaining item by incremental-closure utility per token;
4. select candidates while budget remains;
5. return selected order, used tokens, omitted reasons and aggregate score.

This prototype uses a deterministic heuristic rather than claiming globally optimal knapsack output.

## Failure model
Invalid numeric ranges, cycles with missing targets, mandatory overflow or impossible dependency closure => FREEZE with explicit reason.

## Evidence target
E2 unit tests cover mandatory overflow, dependency closure, deterministic selection and budget enforcement.
