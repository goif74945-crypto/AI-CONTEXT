# P4.1 Command Model

## Contract
A command is immutable task intent plus mutable lifecycle status. Historical identity/scope/evidence obligations are never silently rewritten.

## States
`READY → CLAIMED → EXECUTING → VERIFYING → COMPLETED` with explicit side states:
`FAILED / BLOCKED / STALE / CANCELLED / QUARANTINED`.

Legal transitions are machine-readable in `state-transitions.json`.

## Required exactness
A command pins `created_from_head` and `expected_head`. Execution against a different current HEAD is forbidden; P4.5 performs revalidation.

## Files
- `command.schema.json`
- `state-transitions.json`
- `examples/golden-command.json`
- `examples/negative-illegal-transition.json`
- `validation-report.md`
