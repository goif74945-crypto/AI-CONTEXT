# AI-CONTEXT

AI-CONTEXT is a **model-agnostic execution context repository**.

It is designed to help AI systems do more than remember information. It gives them a durable way to:

- understand project truth;
- resolve authority;
- plan work;
- implement and create artifacts;
- audit repositories;
- verify claims with the correct evidence;
- survive context-window limits;
- write durable state back for the next model/session.

## Quick start

Start at:

**[INDEX.md](./INDEX.md)**

Then load:
1. `AI-EXECUTION-KERNEL.md`;
2. `WORK-ROUTER.md`;
3. only the relevant rules/project/workflow/schema.

## Core principle

`Context alone is passive. Context + contracts + workflows + evidence = executable continuity.`

## Design properties

- progressive context loading;
- no silent guessing;
- source/repo/runtime truth separation;
- explicit task contracts;
- requirement ledgers;
- evidence-class matching;
- durable checkpoints;
- provider/model independence;
- protected mutation boundaries;
- resumable work across sessions/models.

## Long work

For sources or investigations larger than one model context:

`READ → ANALYZE → WRITE CHECKPOINT → UPDATE COVERAGE → CONTINUE`

This prevents valuable project knowledge from disappearing when a context window ends.

## Status discipline

Use:
`PASS / FAIL / PARTIAL / BLOCKED / NOT_VERIFIED / UNKNOWN / CONFLICT`.

Never call something complete merely because code/docs exist.

## Project-specific authority

Project context may define stricter rules than the global kernel. When it does, resolve authority explicitly rather than merging conflicting rules silently.
