# NEXY.AI First-Class Semantic Diff + Change Impact

## Canonical role
This directory is the **canonical change-impact facade**. It composes:
- `semantic-diff/` — before/after semantic classification engine;
- `impact/system-impact.jsonl` — per-entity typed dependency dataset;
- `intelligence-graph/` — typed cross-registry traversal;
- invariants + traceability + contracts/FSM/state/security/events/config registries.

## Canonical pipeline
`DIFF → FILE/SYMBOL → ENTITY → REQUIREMENT → CONTRACT → FSM → INVARIANT → STATE → SECURITY → EVENT → CONFIG → DEPENDENTS → TESTS → REGRESSION → EVIDENCE OBLIGATION`

## Certainty law
Mappings are **EXACT**, **CANDIDATE**, or **UNKNOWN**.
Filename similarity alone MUST NOT become EXACT.

## Supported source changes
CODE / CONFIG / SCHEMA / STATE / PERMISSION / CONTRACT / REQUIREMENT_SPEC

## Files
- `change-impact-index.jsonl` — 518 entity impact records.
- `change-impact-query.schema.json` — answer contract for “If X changes, what must be rechecked before PASS?”
- `semantic-diff-spec.json`
- `examples/golden-code-change.json`
- `examples/golden-config-change.json`
- `examples/negative-filename-only.json`
- `validation-report.md`

## Truth boundary
Impact is a recheck obligation, not proof that a dependent is broken.
Tests/evidence stay NOT_VERIFIED until executed for the exact resulting revision.
