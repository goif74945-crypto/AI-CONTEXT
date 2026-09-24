# P4.2 Command Queue

## Purpose
Dependency-aware deterministic queue over immutable command identities.

## Ordering
Scheduler candidates are ordered by:
1. priority rank: `CRITICAL < HIGH < NORMAL < LOW`;
2. monotonic `enqueue_sequence`;
3. lexicographic `command_id` tie-breaker.

Wall-clock time is not an ordering authority.

## Readiness
A command is READY only when all dependency commands are COMPLETED. Missing, self, cyclic or non-completed dependencies prevent readiness.

## Integrity
- duplicate command IDs: forbidden;
- command dependency cycles: forbidden;
- queue state does not grant mutation authority;
- CLAIMED requires P4.4 lease proof before execution.

## Files
- `queue.schema.json`
- `queue-policy.json`
- `examples/golden-queue.json`
- `examples/negative-cycle.json`
- `examples/negative-duplicate.json`
- `validation-report.md`
