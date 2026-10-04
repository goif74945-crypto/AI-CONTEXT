# Design — Liveness / Deadlock Sentinel (LDS)

**Status:** Lo4 EXPERIMENTAL / no Canon authority.

## Objective
Add a progress-oriented analytical surface to workflows that may be safe yet permanently stuck.

## States
`READY`, `RUNNING`, `WAITING`, `PASS`, `FAIL`, `BLOCKED`.
Terminal states are `PASS` and `FAIL`.

## Output classification
- `DEADLOCK`: a strongly connected cycle exists among unresolved non-terminal wait dependencies.
- `PROGRESSABLE`: no deadlock and at least one READY/RUNNING item exists.
- `QUIESCENT`: all items terminal.
- `STARVATION_RISK`: non-terminal work exists but no runnable item and no dependency cycle was found.

## Algorithm
Validate IDs/dependencies, remove dependencies already terminal, run deterministic iterative SCC analysis (Kosaraju-style, avoiding recursion-limit coupling), then apply status precedence.

## Failure semantics
Unknown state/dependency, duplicate ID or malformed wait list is rejected. The engine does not infer missing tasks.

## NEXY value
Can become a scheduler watchdog or mission-health signal after integration proof. Snapshot classification is not a proof of future fairness or distributed consensus liveness.
