# NEXY.AI Failure / Recovery Library

Files:
- `failures.jsonl` — canonical, internal and source-scenario failure records.
- `recovery-playbooks.jsonl` — deterministic recovery skeletons.
- `failure.schema.json`
- `validation-report.md`

Use before repair work:
1. identify the exact failure layer/code;
2. retrieve affected systems/invariants/contracts;
3. inspect known recovery rule;
4. run relevant regressions;
5. only then add proven root cause / successful recovery back into this library.

Never convert UNKNOWN incident history into invented experience.
