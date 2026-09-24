# P4.11 Deterministic Scheduler

## Purpose
Select only executable commands without granting mutation authority.

## Eligibility
A command is schedulable only when queue state is READY, dependencies are complete, expected-HEAD guard is PASS, an eligible worker exists, and no active path/resource/dependency-closure claim collides.

## Ordering
Eligible candidates are ordered by queue priority, enqueue_sequence, then command_id. Worker selection is capability-compatible, AVAILABLE first, then worker_id lexicographically. No RNG or wall-clock ordering authority.

## Stop conditions
STALE, BLOCKED, QUARANTINED, unresolved collision, missing dependency, missing eligible worker, failed HEAD guard, or required human gate prevent dispatch.

## Files
- `scheduler.schema.json`
- `scheduler-policy.json`
- `examples/cases.json`
- `validation-report.md`
