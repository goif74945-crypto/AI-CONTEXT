# NEXY.AI Semantic Diff Engine

## Purpose
Convert code/config/spec diffs into **semantic engineering impact**.

Git diff answers:
> what text/code changed?

Semantic diff answers:
> what behavior, authority, contract, invariant, state, security or proof obligation changed?

## Core pipeline
`BEFORE/AFTER REFS → FILE/SYMBOL DIFF → ENTITY MAP → SEMANTIC DIMENSIONS → IMPACT GRAPH → REGRESSION/EVIDENCE OBLIGATIONS`

## Files
- `engine.json`
- `semantic-diff.schema.json`
- `examples.json`
- `validation-report.md`

## Truth rule
When mapping is not exact, emit CANDIDATE/UNKNOWN.
Never infer an authority or behavior change solely from filename similarity.
