# P4.6 Command Supersession

## Model
Supersession is an append-only directed edge:
`OLD COMMAND → NEW COMMAND`.

It never rewrites the old command.

## Invariants
- no self-supersession;
- graph is acyclic;
- each old command has at most one direct successor;
- a new command may supersede multiple old commands only explicitly;
- superseded/stale command claims cannot execute.

HEAD-stale replacement carries head-guard + semantic-diff + change-impact evidence.

## Files
- `supersession.schema.json`
- `supersession-policy.json`
- golden chain example
- negative cycle/fork examples
- `validation-report.md`
