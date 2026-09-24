# NEXY.AI Golden / Negative Corpus

- `golden/examples.jsonl` — correct behavior patterns.
- `negative/examples.jsonl` — plausible-looking but prohibited patterns.
- `example.schema.json`
- `validation-report.md`

Use as few-shot context for Builder/Auditor/Context Pack generation.

Priority negative patterns:
fake success · hidden fallback · stale evidence · invalid FSM · scope creep · authority inversion · UI masking failure · unverified release · nondeterministic mutation.
