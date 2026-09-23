# WORKFLOW — MEMORY / CONTEXT UPDATE

## Goal
Convert completed work or large-source analysis into durable, compact, provenance-aware context.

## Pipeline
`COLLECT → CLASSIFY → DEDUP → RESOLVE → NORMALIZE → WRITE → INDEX → VERIFY`

## 1. Collect candidates
Only consider information that may matter later:
- canonical requirements;
- architecture;
- decisions;
- verified state;
- evidence;
- failures/root causes;
- workflows;
- unresolved conflicts.

## 2. Classify
Use memory classes in `rules/MEMORY.md`.

## 3. Deduplicate
Prefer one authoritative record plus references over repeated near-copies.

## 4. Resolve conflicts
Do not overwrite conflicting history.
Use authority/evidence and preserve superseded lineage.

## 5. Normalize
Store actionable structure:
- what;
- why;
- authority;
- dependencies;
- failure behavior;
- evidence/status.

## 6. Large-source streaming
For long documents:
`read chunk → analyze → write checkpoint → update coverage map → continue`

## 7. Index
Ensure the new context is discoverable from the relevant INDEX.

## 8. Verify write
Re-read or list written paths after mutation.
Do not assume a write succeeded.

## 9. Completion
The context update is good when a new model can resume without needing the original conversation.
