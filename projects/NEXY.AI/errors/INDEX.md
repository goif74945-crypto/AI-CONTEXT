# NEXY.AI Error + Incident Taxonomy

## Purpose
Machine-readable mapping from canonical error codes to operational handling.

## Files
- `error-taxonomy.jsonl` — 29 current DOC-C error records.
- `error.schema.json` — taxonomy schema.
- `validation-report.md`.

## Severity truth rule
DOC-C defines a global Severity enum but the captured error contract does not assign a canonical severity to every individual error.

Therefore:
- `source_severity` remains `SOURCE_NOT_SPECIFIED_PER_ERROR` unless a future source explicitly maps it.
- `engineering_severity` is **AI-CONTEXT impact metadata**, not DOC-C Canon.
- `severity_derivation` records why the engineering level was assigned.

Do not silently promote AI-CONTEXT S0–S5 to a source-law claim.

## Failure priority
DOC-C explicitly prioritizes simultaneous failure classes:
1. security breach
2. schema violation
3. illegal state transition
4. consensus failure
5. timeout

The taxonomy preserves that separately from engineering severity.

## Operational chain
`ERROR → user surface → incident behavior → freeze/block semantics → recovery`.

Context-dependent fields remain explicit rather than being invented as absolute behavior.
