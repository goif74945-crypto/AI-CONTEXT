# P4.3 Worker Registry

## Purpose
Declare worker identity, execution role, capabilities, scope boundaries and concurrency capacity before claims exist.

## Assignment law
A worker may be considered for a command only when:
- role/capability matches;
- target scope is inside `allowed_scopes`;
- target does not intersect `forbidden_scopes`;
- worker can accept new work;
- active claims remain below `max_concurrent_claims`.

Worker metadata never expands command/governance authority.

## Human-gate semantics
`human_gate_capability=true` means the worker may route an escalation. It never authorizes self-approval.

## Files
- `worker-registry.schema.json`
- `worker-policy.json`
- golden/negative examples
- `validation-report.md`
