# NEXY.AI Checkpoint / Resume Protocol

## Purpose
Allow large work to stop at any context boundary and continue from an exact semantic node.

## Current checkpoint
- `current.json` — latest resumable checkpoint.
- Historical checkpoints use dated/task-specific filenames and are immutable after supersession.

## Required fields
- TASK_ID
- SOURCE_REVISION
- TARGET {repo, branch, HEAD}
- LAST_COMPLETED_NODE
- NEXT_NODE
- ARTIFACTS
- FINDINGS
- OPEN_UNKNOWNS
- DEPENDENCIES
- AUTHORIZATION
- RESUME_INSTRUCTION

## Checkpoint timing
Write a checkpoint:
- after every major registry/domain completion;
- before switching role Builder↔Auditor↔Fixer;
- before a context-window boundary;
- before/after a high-impact mutation campaign;
- whenever a blocker prevents continuation.

## HEAD semantics
A checkpoint records the exact semantic HEAD whose state it summarizes. The commit that writes the checkpoint is metadata-only and therefore necessarily newer than the recorded semantic HEAD. On resume, inspect newer commits before assuming semantic drift.

## Resume algorithm
1. Read checkpoint only as navigation state.
2. Refresh AI-CONTEXT and target repo HEAD.
3. If target HEAD changed:
   - inspect the diff first;
   - distinguish checkpoint/metadata-only writes from semantic change;
   - mark implementation/evidence/navigation fields stale when semantics changed;
   - do not replay old PASS claims.
4. Load the compiled pack appropriate to `NEXT_NODE` when available.
5. Load only referenced registries/artifacts.
6. Revalidate unresolved conflicts/blockers.
7. Continue from `NEXT_NODE`, not from task zero.

## Resume statuses
- RESUMABLE
- RESUMABLE_WITH_REFRESH
- BLOCKED
- INVALID_CHECKPOINT
- AUTHORITY_CHANGED

## Integrity rule
A checkpoint never grants mutation permission.
Authorization must be re-evaluated in the receiving task/session.
