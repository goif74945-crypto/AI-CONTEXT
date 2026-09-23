# NEXY.AI Contradiction Engine Data

## Purpose
Detect spec/architecture contradictions **before coding** and distinguish real contradictions from legitimate domain/boundary differences.

## Files
- `pairs.jsonl` — 16 machine-readable claim pairs.
- `engine.json` — classification/blocking algorithm.
- `pair.schema.json`
- `validation-report.md`

## Relations
- UNRESOLVED_CONTRADICTION
- SUPERSESSION
- DOMAIN_SEPARATION
- BOUNDARY_SEPARATION
- CLASS_SEPARATION
- AUTHORITY_SEPARATION
- SCOPE_SEPARATION

## Blocking rule
Only unresolved material contradictions block a task automatically.
Resolved distinctions remain stored so future AI does not repeatedly “rediscover” them and incorrectly merge semantics.

## Current blocker
`CONFLICT-RCL-LATENCY-001`
