# RHL — Reversibility Half-Life Scheduler

## Objective
Treat reversibility as a decaying operational resource. “Rollback exists” is insufficient if rollback quality falls below an acceptable floor before evidence or approval arrives.

## Model
`R(t) = initial_reversibility * retention_per_tick^t`, all Q64.64.

The scheduler finds the latest tick not past the hard deadline for which `R(t) >= minimum_reversibility` using deterministic binary search.

## Decisions
- current tick past hard deadline -> FREEZE;
- current reversibility below floor -> FREEZE;
- close to/latest at safe edge under checkpoint guard -> CHECKPOINT_REQUIRED;
- otherwise -> PASS with `latest_safe_tick`.

## Non-goals
The model does not infer real rollback quality. An integration adapter must derive `initial`, `retention`, and `floor` from authoritative operational evidence/policy. This prototype only evaluates an explicit model.
