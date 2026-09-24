# NEXY.AI Invariant Registry

Canonical:
- `invariants.jsonl` — atomic “must not break” assertions.
- `law-groups.jsonl` — LAW/INVARIANT ontology entity → requirements → atomic invariants → code map.
- `invariant.schema.json`
- `validation-report.md`

## Design
Broad architecture laws are not treated as one prose blob.

Trace:
`LAW / INVARIANT ENTITY → MUST REQUIREMENT → ATOMIC INVARIANT → IMPLEMENTATION REFS → TEST → EVIDENCE`

Test/Evidence links remain empty until their dedicated stages.

## Critical rule
Do not weaken, reinterpret, or silently bypass an invariant to make a patch pass. If the source must change, change authority/supersession first.
