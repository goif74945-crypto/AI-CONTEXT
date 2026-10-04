# Design — NEXY Critical-Path Evidence Scheduler (CPES)

**Status:** AI-PROPOSED / NON-AUTHORITY / NOT PRODUCTION INTEGRATED.

## Objective
Plan verification DAG work efficiently across bounded resource slots while respecting evidence prerequisites.

## Algorithm
Validate DAG and planned evidence feasibility; compute bottom-level critical paths; schedule using per-resource pending release-time heaps and runnable critical-path heaps; choose earliest feasible work, then critical-path/evidence/ID tie-breaks.

## Invariants
Dependencies finish before consumers; same slot never overlaps; cycles/missing capacity reject; planned evidence gap freezes; PLAN_READY never means evidence executed.

## Complexity
O(V+E) graph work plus approximately O(V·R + V log V) scheduling for R resource classes.

## Future NEXY boundary
Candidate between task decomposition and executor dispatch. Executors/logs still create actual E1-E7 evidence.

## Limits
Deterministic heuristic, not globally optimal scheduling proof; no preemption/deadlines/live rescheduling yet.

## Security boundary
No network access, credential handling, repository mutation, production side effect, or NEXY law override occurs in the reference engine. A future adapter must validate provenance and authorization.
