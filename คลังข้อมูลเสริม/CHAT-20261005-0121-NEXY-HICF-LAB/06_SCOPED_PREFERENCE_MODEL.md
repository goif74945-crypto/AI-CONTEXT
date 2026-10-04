# 06 — SCOPED PREFERENCE MODEL

## Problem

Personalization can improve NEXY's user experience, but uncontrolled preference inference can quietly become hidden policy. That conflicts with explicit authority and provenance principles.

## Proposed scopes

### EPHEMERAL
Applies only to the current interaction/task. Safe default for inferred presentation choices.

### PROJECT
Applies within an explicit project context. Requires a scoped source/provenance record.

### DURABLE
Persists across projects/sessions. Requires explicit user authority in this proposal.

## Hard rule

`DURABLE + inferred_only = INVALID`

Examples of behavior that must not silently become durable law:
- user often accepts concise responses;
- user repeatedly chooses one tool;
- user tends to skip explanations;
- user edits generated code into a certain style.

These may become candidate observations, not durable preference authority.

## Suggested future record

- key
- value
- scope
- explicit flag
- provenance
- created_at / source version
- expiry/review policy
- supersedes relation

The v0 prototype validates only the authority-critical subset.
