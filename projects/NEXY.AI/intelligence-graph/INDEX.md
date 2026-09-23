# NEXY Project Intelligence Graph

## Purpose
A queryable engineering-intelligence graph connecting the project's source truth, requirements, architecture, implementation navigation, verification and status.

## Primary spine
`SOURCE → AUTHORITY → REQUIREMENT → ENTITY/SYSTEM → IMPLEMENTATION → TEST → EVIDENCE → STATUS`

## Side dimensions
`DEPENDENCY / INVARIANT / FAILURE / CONFIG / EVENT / OBSERVABILITY / SCOPE / CONFLICT / SUPERSESSION`

## Files
- `nodes.jsonl` — 1207 graph nodes.
- `edges.jsonl` — 7179 typed edges.
- `registry.json` — graph identity/counts/source registries/freshness.
- `query-recipes.json` — common traversal recipes.
- `validation-report.md`

## Example capability
For:
> “If Queue idempotency changes, which requirements, systems, invariants, tests and failures are relevant?”

AI can traverse entity/dependency/requirement/invariant/failure/test edges instead of re-reading the entire project.

## Truth boundary
The graph is a compiled index, **not new Canon**.
Source/governance/evidence registries win if any compiled edge becomes stale.
