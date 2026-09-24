# NEXY.AI Context Router + Pack Generator

Files:
- `context-router.json`
- `pack-generator.json`
- `routing-examples.jsonl`

Goal:
load the **minimum sufficient verified context** for a task instead of re-reading the entire project.

Router selects domain/context.
Generator composes Build or Audit packs.

Hard priority:
authority → scope → requirements → invariants → FSM/contracts/failures → code → tests → evidence.

Never trim S5 invariants or unresolved conflicts to save context.
