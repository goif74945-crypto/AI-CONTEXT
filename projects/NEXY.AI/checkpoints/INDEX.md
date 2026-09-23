# NEXY.AI Checkpoint / Resume Protocol

## Purpose
Allow large work to stop at any context boundary and continue from an exact semantic node.

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

## Resume algorithm
1. Read checkpoint only as navigation state.
2. Refresh AI-CONTEXT and target repo HEAD.
3. If target HEAD changed:
   - mark implementation/evidence/navigation fields stale;
   - refresh required maps;
   - do not replay old PASS claims.
4. Load the compiled pack appropriate to `NEXT_NODE`.
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
