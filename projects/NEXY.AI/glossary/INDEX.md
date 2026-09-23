# NEXY.AI Glossary / Alias Registry

## Purpose
Resolve names across source eras without turning aliases into duplicate systems.

## Files
- `aliases.json` — 86 alias records with canonical target, era, source-range validity and status.
- `terms.jsonl` — 516 canonical ontology terms for fast lookup.
- `alias.schema.json`.
- `validation-report.md`.

## Validity semantics
`valid_from` / `valid_to` are **source paragraph navigation markers for the pinned source revision**, not calendar dates and not guaranteed runtime activation versions.

Canonical authority still comes from governance/supersession/scope registries.

## Rule
Alias != second entity unless source assigns distinct semantics.
Identical labels in different FSMs remain disambiguated by entity ID/parent.
