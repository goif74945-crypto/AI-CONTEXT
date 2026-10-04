# Design — Minimal-Cut Failure Geometry (MCFG)

**Status:** Lo4 EXPERIMENTAL / no Canon authority.

## Objective
Given multiple alternative support paths, enumerate every inclusion-minimal set of facts/components whose simultaneous failure intersects all paths. This exposes hidden fragility that ordinary “number of proofs” metrics miss.

## Contract
Input: iterable of non-empty sets of non-empty string node IDs. Optional `max_nodes` bound defaults to 20.
Output: deterministic tuple of sorted tuples, ordered first by cardinality then lexicographically.

## Algorithm
Normalize and remove redundant superset support paths, then incrementally build minimal transversals (minimal hitting sets). After each path expansion, remove any candidate that has a strict subset already satisfying processed paths.

## Invariants
- every returned cut intersects every support path;
- no returned cut has a proper subset that also intersects every path;
- order of paths and nodes cannot change output;
- exact enumeration rejects a universe larger than configured bound.

## Complexity
Minimal hitting-set enumeration is exponential in the worst case. The explicit node bound is a safety feature, not an implementation accident.

## NEXY value
Use it to find “one fact breaks everything” or small proof/evidence cut sets before release/adjudication. It is analysis only and cannot decide Canon validity by itself.
