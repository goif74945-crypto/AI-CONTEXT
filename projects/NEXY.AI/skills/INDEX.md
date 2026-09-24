# NEXY.AI Skill Registry

Canonical:
- `skills.jsonl`
- `skill.schema.json`

A skill is not just knowledge; it is a workflow with explicit identity, inputs/outputs, permissions, failure modes, validation obligations and evidence boundaries.

Status semantics:
- `MATERIALIZED` — a loadable SKILL.md/record exists, but required behavioral/security/integration/regression/evidence gates have not all been executed.
- `VERIFIED_WORKFLOW` — an evidence-backed workflow version has been successfully validated.
- `VERIFIED_DATA_WORKFLOW` — an evidence-backed data workflow version has been successfully validated.
- `BLOCKED` — the skill cannot safely progress because authority, dependency, security, integrity or validation requirements are unresolved.

NEXY-native Skill identities are source-derived from `skills/nexy/MASTER-SPECIFICATION.md`. A newly created SKILL.md MUST remain MATERIALIZED until the Master Specification's applicable V0–V9 / Gate 0–6 obligations are actually satisfied.

`last_verified` and benchmark fields are revision/time-sensitive and must be refreshed when workflow semantics change.
