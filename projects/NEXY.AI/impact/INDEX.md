# NEXY.AI Change Impact Engine Data

## Purpose
Pre-computed impact intelligence for AI builders/auditors.

Query by `entity_id` before changing a system to obtain:
- prerequisites/dependents;
- transitive dependency blast radius;
- semantic graph neighbors;
- governing requirements;
- affected invariants;
- historical failure intelligence;
- mapped implementation/tests/evidence;
- required regression classes.

## Files
- `system-impact.jsonl` — 516 entity impact records.
- `impact.schema.json` — record schema.
- `validation-report.md` — derivation/integrity report.

## Derivation
Generated from current AI-CONTEXT:
ontology + dependency graph + invariants + failure library + traceability spine.

No impact relationship is treated as runtime proof.

## Direction
For `REQUIRES`:
`dependent → prerequisite`.

Therefore:
- `direct_prerequisites` = what this entity requires.
- `direct_dependents` = what may be affected if this entity changes.

## Staleness
Implementation/test/evidence references inherit the revision pin/freshness of their source registries.
Refresh those registries when target HEAD changes.
