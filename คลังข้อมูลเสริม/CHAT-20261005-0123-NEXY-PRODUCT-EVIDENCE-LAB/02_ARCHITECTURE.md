# 02 — Architecture

## Classification

`AI-PROPOSED`, `NON-GOVERNING`, `REFERENCE_IMPLEMENTATION`.

## Problem

Feature proposals are often written as desires ("make onboarding better") rather than falsifiable contracts. This creates four recurring failure modes: undefined success, metric gaming, stale evidence, and automatic promotion of weak results into product decisions.

NPEL treats experimentation as a controlled evidence pipeline:

```text
Proposal
  ↓
Schema + ethics validation
  ↓
Deterministic experiment compiler
  ↓
Canonical contract + SHA-256 identity
  ↓
Instrumentation contract validation
  ↓
Execution outside NPEL
  ↓
Evidence bound to exact contract hash
  ↓
Guardrail adjudication
  ↓
Primary metric interval analysis
  ↓
SUPPORTED | REJECTED | INCONCLUSIVE | FREEZE
  ↓
Human decision required
```

## Components

### `model.py`
Typed enums/dataclasses defining proposals, metrics, guardrails, observations, contracts, and evaluation results.

### `stats.py`
Deterministic numerical primitives implemented using the Python standard library:
- inverse standard-normal CDF (Acklam approximation);
- two-sided confidence z critical value;
- proportion and mean sample-size planning;
- observed difference, standard error, confidence interval, and p-value approximation.

### `compiler.py`
Validates proposals and refuses prohibited risk flags or missing material fields. Produces a normalized immutable experiment contract with deterministic sample size.

### `serialization.py`
Canonical JSON serialization and SHA-256 hashing. Hash identity prevents evidence produced under one contract from being evaluated under another.

### `analytics.py`
Validates analytics event names/properties and blocks common secret-bearing property names.

### `evaluator.py`
Checks evidence identity, data-quality blockers, planned sample size, and hard guardrail thresholds. Primary metric outcomes are interval-based:
- `SUPPORTED`: confidence interval clears the MDE threshold in the desired direction;
- `REJECTED`: confidence interval is wholly below the MDE threshold in the desired direction;
- `INCONCLUSIVE`: interval overlaps the threshold or sample size is incomplete;
- `FREEZE`: contract mismatch, critical data-quality failure, or hard guardrail breach.

The engine never emits `SHIP` / `DEPLOY` / `RELEASE` authorization.

## Determinism contract

Given the same proposal/evidence and Python numeric behavior, NPEL must produce the same structural result. Critical paths use no current time, network calls, environment-dependent provider state, or randomness.

## Authority boundary

The output is evidence classification, not product authority. Product decisions remain with the human authority operating NEXY.

## Allocation boundary

Reference v1 supports only `allocation_fraction=0.5`. Unequal allocation is rejected at compile time because the current sample-size equations assume equal arms. Future support requires separately verified unequal-allocation planning mathematics.
