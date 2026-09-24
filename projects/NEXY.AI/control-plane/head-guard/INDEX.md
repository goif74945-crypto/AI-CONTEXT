# P4.5 Expected-HEAD Guard

## Absolute precondition
Before a Builder mutates a target:
`CURRENT_HEAD == COMMAND.EXPECTED_HEAD`

A claim/lease cannot override this check.

## Mismatch flow
`HEAD MISMATCH → ORIGINAL COMMAND NOT EXECUTABLE → SEMANTIC DIFF → CHANGE IMPACT → SUPERSEDE / STALE / BLOCKED`

The original command's `expected_head` is immutable history.

## Proof
A superseding command requires explicit semantic-diff and impact references and pins the refreshed current HEAD.

## Files
- `head-guard.schema.json`
- `head-guard-policy.json`
- matching/stale golden examples
- silent-rewrite/execution negative example
- `validation-report.md`
