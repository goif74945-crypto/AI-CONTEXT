# Temporary execution memory

- Objective: create and test five novel Lo4 experimental systems in AI-CONTEXT only.
- Protected: every repository whose name contains `NEXY.AI`; read-only inspection is allowed, mutation is forbidden.
- Canon boundary: all five systems remain EXPERIMENTAL until a separate formal promotion process proves and authorizes them.
- Baseline: AI-CONTEXT main observed before local implementation at `3fc525b93a625847221344f2bf383bd23c7e3a73`.
- Novelty path scan: 2,868 supplemental paths inspected; no path-name hits for deadlock, livelock, starvation, liveness, dominator, symmetry, state-space, minimal-cut/cut-set, tournament, or evolutionary.
- TDD mode: tests and interface stubs first; require observed RED before implementation and fresh GREEN after implementation.

## Checkpoint — implementation and property verification
- Five engine implementations written locally.
- Baseline unit suite: 17/17 PASS with fresh execution.
- Extended unit/property suite: 37/37 PASS with fresh direct Python execution.
- Independent formulations include brute-force minimal hitting sets and simple-path dominator intersections.
- Durable GitHub upload: NOT YET PERFORMED at this checkpoint.
- Static compile/final hash seal: pending.

## Checkpoint — final local seal
- Stress benchmark discovered F-001 recursion failure in liveness SCC at 1,000-node cycle.
- F-001 repaired by iterative SCC traversal; 1,500-node regression test added and passed.
- Final full suite and compile gate executed successfully after repair.
- Final stress benchmark executed successfully after repair.
- Next action: durable GitHub upload to unique AI-CONTEXT supplemental path, then read-back verification.
