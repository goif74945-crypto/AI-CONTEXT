# NEXY.AI FSM Registry

Files:
- `fsm-registry.jsonl`
- `fsm.schema.json`
- `validation-report.md`

Rule: **never merge state machines by matching state names.**

Examples:
- Execution `FREEZE`
- Risk `FAILSAFE`
- App `FROZEN`
- Global `FROZEN`

are distinct states in distinct authority namespaces.

Implementation-only state models remain labeled as observed implementation and do not become source canon automatically.
