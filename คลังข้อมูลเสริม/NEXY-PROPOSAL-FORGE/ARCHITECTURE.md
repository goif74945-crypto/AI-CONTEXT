# Architecture — NEXY Proposal Forge

## Classification

`AI_PROPOSED_CONCEPT` + `IMPLEMENTED_SUPPLEMENTAL_TOOL` + `NON_AUTHORITATIVE`

## Objective

Create a reusable boundary between AI creativity and NEXY project truth. The system should make it cheap to generate ideas while making it difficult to accidentally represent those ideas as current law, build scope, or implementation fact.

## Pipeline

```text
PROPOSAL JSON
  -> STRICT PARSE / VALIDATE
  -> CANONICALIZE
  -> SHA-256 FINGERPRINT
  -> CATALOG OVERLAP ANALYSIS
  -> EVIDENCE CONTRACT
  -> AUTHORITY-CONFLICT GATE
  -> ONE ADVISORY RECOMMENDATION
```

## Components

### `models.py`
Owns the candidate capsule contract and rejects invalid state before evaluation.

### `canon.py`
Normalizes text with Unicode NFC + whitespace collapse, rejects floats, serializes sorted-key JSON, and creates SHA-256 fingerprints. List order is preserved because order may carry proposal semantics.

### `overlap.py`
Computes deterministic comparison scores using word units and Unicode character trigrams. Scores are integers in basis points. The overall overlap score is:

```text
35% title
35% proposed capabilities
20% problem statement
10% integration surfaces
```

An exact normalized title forces a minimum score of `9500bp`.

### `engine.py`
Applies fail-closed decision order:

1. unresolved authority conflict -> `FREEZE_CONFLICT`
2. overlap >= 9500bp -> `REJECT_DUPLICATE`
3. overlap >= 7000bp -> `MERGE_WITH_EXISTING`
4. evidence gaps -> `NEEDS_EVIDENCE`
5. otherwise -> `PROMOTE_FOR_HUMAN_REVIEW`

This order is deliberate. Novelty never overrides a known authority conflict, and evidence completeness never overrides a duplicate.

### `collision.py`
Owns deterministic work-manifest scope comparison. It detects active recursive/exact write-scope overlap and proposal-ID collisions. It is advisory only and explicitly not a distributed lock.

### `cli.py`
Provides `validate`, `fingerprint`, `canonical`, `evaluate`, and `collide` commands with machine-readable JSON failure output.

## Evidence contract

A candidate is not eligible for positive human-review recommendation unless:

- it has at least two evidence references;
- at least one evidence record has role `AUTHORITY` and a factual truth class (`SOURCE_FACT`, `REPO_FACT`, `RUNTIME_FACT`, or `EXTERNAL_FACT`);
- at least one evidence record has role `DUPLICATE_CHECK`;
- if assumptions exist, at least one evidence record has role `ASSUMPTION` and truth class `ASSUMPTION`.

This contract is intentionally small. It proves disciplined proposal packaging, not feature correctness.

## Security / integrity

The evaluator has no write path to NEXY.AI, no shell execution, no network client, no dynamic import of proposal code, and no model invocation. Proposal data is treated strictly as data.

## Non-goals

- semantic proof that a feature has never existed;
- automated architecture approval;
- automatic edits to NEXY.AI;
- release/deployment authorization;
- replacing DOC-B/C/D/E authority resolution;
- claiming product-market fit from AI opinion.
