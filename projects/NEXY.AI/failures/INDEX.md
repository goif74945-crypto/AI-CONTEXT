# NEXY.AI Failure / Recovery Library

Files:
- `failures.jsonl`
- `failure.schema.json`
- `validation-report.md`

Query before risky work:

> Has this subsystem failed this way before?

Each record stores:
`context → symptom → root cause → failed approach → why failed → successful recovery → regression test → prevention`.

Current initial library covers FREEZE/audit persistence, queue schema/stale/idempotency/durability, release policy, Vault integrity, recovery loops, pre-death/pre-kill state, sandbox escape, capability/app lifecycle drift, GameSpec RNG review, robotics safety dominance and stale evidence.
