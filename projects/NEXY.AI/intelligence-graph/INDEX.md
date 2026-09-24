# NEXY Project Intelligence Graph

## Purpose
Queryable engineering-intelligence graph connecting source truth, requirements, architecture, implementation navigation, verification and status.

## Primary spine
`SOURCE → AUTHORITY → REQUIREMENT → ENTITY/SYSTEM → IMPLEMENTATION → TEST → EVIDENCE → STATUS`

## Side dimensions
`DEPENDENCY / INVARIANT / FAILURE / CONFIG / EVENT / OBSERVABILITY / SCOPE / CONFLICT / SUPERSESSION`

## Files
- `nodes.jsonl`
- `edges.jsonl`
- `graph-meta.json` — graph identity/counts/source revision/freshness metadata.
- `query-recipes.json` — deterministic traversal recipes.
- `validation-report.md`

## Change-impact integration
Canonical output: `projects/NEXY.AI/change-impact/change-impact-query.schema.json`.
The graph supplies typed traversal and MUST NOT manufacture EXACT mappings from filename similarity.

## Truth boundary
Compiled graph edges are indexes, not new Canon.
