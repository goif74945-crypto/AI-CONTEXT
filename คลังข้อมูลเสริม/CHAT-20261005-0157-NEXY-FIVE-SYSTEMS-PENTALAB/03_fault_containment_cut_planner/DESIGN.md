# Design — NEXY Fault Containment Cut Planner (FCCP)

**Status:** AI-PROPOSED / NON-AUTHORITY / NOT PRODUCTION INTEGRATED.

## Objective
Compute the smallest deterministic hard-dependency quarantine closure after observed component failures.

## Algorithm
BFS from sorted failed roots across HARD provider→consumer edges; SOFT consumers degrade; ISOLATED edges do not propagate; mandatory quarantine freezes. Causal lineage is stored as predecessor links and reconstructed on demand.

## Invariants
Unknown refs reject; quarantine/degraded/healthy are disjoint and exhaustive; hard cycles terminate; permutations are deterministic.

## Complexity
O(V+E) closure, O(V) lineage storage; reason-path reconstruction O(path length).

## Future NEXY boundary
Candidate beside incident/RSEL/ECL health logic. It proposes containment; NEXY authority decides real isolation actions.

## Limits
Static graph per evaluation; no distributed failure detector or quarantine executor.

## Security boundary
No network access, credential handling, repository mutation, production side effect, or NEXY law override occurs in the reference engine. A future adapter must validate provenance and authorization.
