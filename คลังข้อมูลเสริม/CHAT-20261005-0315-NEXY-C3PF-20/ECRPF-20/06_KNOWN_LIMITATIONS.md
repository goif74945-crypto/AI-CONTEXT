# Known Limitations

- ECRPF consumes normalized snapshots; it does not discover every `process.env` reference automatically.
- Rule authoring remains an authority-sensitive adapter task and must be verified against Canon/current NEXY source.
- Secret references prove only boundary shape/provenance, not that the secret exists or is valid.
- Rollout cohort proof is deterministic but does not prove business/operational success of a rollout.
- The Q64 blast-radius score is a deterministic prioritization metric; it cannot override mandatory gates or Canon.
- One-ULP tolerance exists only in max-step comparison to account for independent Q64 rational truncation. It is explicitly bounded to one raw unit.
- Isolated tests do not prove compatibility with future NEXY commits.
- No code in `NEXY.AI-` was modified or integrated by this work.
