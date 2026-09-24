# NEXY.AI FSM Registry

Files:
- `fsms.jsonl`
- `fsm.schema.json`
- `validation-report.md`

Rule: never merge FSMs because state names look similar.

Each FSM has its own namespace, authority, scope, states, transitions/known transition semantics, failure behavior, source pointers, requirements and implementation refs.

Implementation-only state models are retained separately rather than rewritten as source-defined FSMs.
