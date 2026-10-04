# Design — Dependency Dominator Analyzer (DDA)

**Status:** Lo4 EXPERIMENTAL / no Canon authority.

## Objective
Find graph nodes that every path from a designated root to a critical target must traverse. For multiple targets, identify shared non-trivial dominators as architectural chokepoints.

## Contract
Input: directed adjacency graph, start node, optional target set.
Output: dominator sets for every reachable node and deterministic shared critical dominators.

## Algorithm
Classic iterative dominator dataflow: `Dom(start)={start}` and every other reachable node begins as all reachable nodes, then converges to `{node} U intersection(Dom(predecessors))`.

## Invariants
Unreachable nodes do not receive dominator claims. Unknown/unreachable requested targets are rejected rather than silently ignored.

## NEXY value
Useful for deciding where redundancy, monitoring, isolation or evidence hardening yields the widest critical-path impact. Topological dominance is not the same thing as reliability probability.
