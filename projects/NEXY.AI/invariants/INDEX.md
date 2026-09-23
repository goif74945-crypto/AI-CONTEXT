# NEXY.AI Invariant Registry

## Purpose
Machine-readable list of properties that a patch, migration, runtime path, or design evolution must not violate.

## Files
- `invariants.jsonl` — 50 normalized invariants.
- `invariant.schema.json` — record schema.
- `INDEX.md` — semantics and severity.

## Severity
Severity here is **AI-CONTEXT engineering impact metadata**, unless a source explicitly provides its own severity:
- S0 informational
- S1 local/noncritical
- S2 degraded feature
- S3 major subsystem correctness
- S4 release/reliability blocker
- S5 authority/integrity/safety/data-corruption class

## Patch use
`CHANGE → affected systems → invariants → required tests/evidence → legal status`

## Evidence boundary
Empty `evidence_refs` means no proof has yet been registered. Code/test references do not automatically make an invariant VERIFIED.

## Count
Total: **50**
- S4: 8
- S5: 42
