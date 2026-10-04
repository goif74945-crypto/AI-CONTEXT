# 05 — INTENT DRIFT AND CONTINUITY

## Threat model

Long-running autonomous work often drifts because intermediate local optimizations replace the original objective. Drift is dangerous even when every individual step looks reasonable.

## Continuity anchor

At task start, record:
- objective;
- immutables;
- constraints;
- prohibitions;
- authority references;
- current unknowns.

Generate a stable fingerprint for the canonical envelope.

## Drift handling

### NONE
Continue.

### LOW
Record delta. Continue only if it does not alter correctness/authority of the active action.

### MATERIAL
Re-evaluate plan and acceptance criteria before mutation.

### AUTHORITY_BREAK
Freeze the affected path. Do not silently replace the original immutable contract.

## Examples

- Formatting preference changes: LOW.
- “Analyze” silently becomes “deploy”: MATERIAL.
- “Do not modify NEXY.AI” disappears from immutables: AUTHORITY_BREAK.
- New prohibition added: MATERIAL and may invalidate queued actions.

## Resume protocol

A resumable checkpoint should contain:
- previous fingerprint;
- current fingerprint;
- classified drift;
- unresolved material unknowns;
- last verified action;
- next proposed action;
- reason the next action is still inside scope.
