# NEXY.AI Proof Obligations

## Purpose
Critical actions must prove explicit preconditions **before execution or promotion**.

## Model
`ACTION → MUST PROVE → REQUIRED EVIDENCE CLASS → ON MISSING`

## Files
- `obligations.jsonl` — 10 obligations.
- `proof-obligation.schema.json`
- `validation-report.md`

## Rule
An obligation is not satisfied because code for the check exists.
The required proof must be current and match the action/target.

## High-impact actions covered
- PRODUCTION_DEPLOYMENT
- SCHEMA_STATE_MIGRATION
- FREEZE_RECOVERY
- VAULT_COMMIT
- AUTHORITATIVE_OUTPUT_RELEASE
- ADD_OR_MODIFY_LAW
- CAPABILITY_ACTIVATION
- PROMOTE_LO2_EVOLUTION_TO_AUTHORITATIVE_RUNTIME
- FUTURE_CANONICAL_CORE_MUTATION
- PHYSICAL_ROBOT_ACTUATION
