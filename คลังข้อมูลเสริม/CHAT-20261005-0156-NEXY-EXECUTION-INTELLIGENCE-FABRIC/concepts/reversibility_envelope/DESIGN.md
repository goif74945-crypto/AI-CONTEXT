# Reversibility Envelope — Design

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## Problem
Automation often discovers rollback difficulty after a mutation has already happened. That is backwards.

## Objective
Validate an action dependency DAG before execution and require either:
- a compensation action for every reversible mutation, or
- explicit authorization for every irreversible mutation.

## Algorithm
Deterministic lexicographic topological sort, then reverse-order compensation plan for reversible actions.

## Outputs
- execution order;
- rollback order;
- first irreversible `point_of_no_return`;
- `FREEZE` on cycle, unknown dependency, missing compensation, or unapproved irreversible action.

## Invariants
Rollback planning happens before external mutation. No action is executed by this library.

## NEXY value
Can give RUN a preflight “recovery envelope” so a task is not considered executable merely because forward steps are known.
