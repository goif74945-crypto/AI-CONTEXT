# NEXY.AI Context Router / Context Pack

Goal: load **minimum sufficient engineering truth**, not the whole project.

Files:
- `routes.json` — TASK TYPE → seed entities/context dimensions/playbook.
- `pack-schema.json` — canonical context-pack shape.
- `builder-profile.json`
- `auditor-profile.json`
- generator scripts under `tools/`.

Resolution:
`TASK → SEEDS → REQUIREMENTS → DEPENDENCIES → AUTHORITY → CONTRACT/FSM/INVARIANT → CODE → TEST/EVIDENCE → FAILURE/SECURITY/STATE/CONFIG → MINIMAL PACK`

The router must never use stale implementation context as current truth.
