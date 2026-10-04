# NEXY Loss-Bounded Context Codec (LBCC)

> **AI-proposed concept, standalone implementation.** This project is not a claim that NEXY.AI currently contains or implements LBCC. It is intentionally stored outside the NEXY.AI repository and is designed for optional future integration.

LBCC compacts durable AI/project context without pretending that lossy summarization is lossless. It keeps selected context atoms byte-for-byte at the field level, records every omission in a cryptographic loss ledger, enforces a caller-defined loss budget, and freezes instead of producing a misleading capsule when protected information cannot fit.

## Why this exists

Long-lived AI systems accumulate context faster than any finite context window can consume it. Ordinary summarization can silently erase provenance, uncertainty, contradictions, evidence references, or authority. LBCC treats context reduction as a controlled state transition with measurable loss.

Core properties:

- deterministic canonical JSON;
- no model calls and no hidden stochastic behavior;
- exact preservation of retained atoms;
- `UNKNOWN` and `CONFLICT` are protected by default;
- immutable atoms are always protected;
- provenance and evidence travel with every retained atom;
- omitted atoms are represented by ID/hash/importance in a separate loss ledger;
- source bundle and dropped-set commitments use SHA-256;
- output capsule byte limit is enforced against canonical UTF-8 bytes;
- maximum allowed information loss is expressed as integer ppm;
- default secret-pattern detection freezes unsafe inputs;
- source-aware verification detects tampering and stale/mismatched evidence.

## Quick start

```bash
PYTHONPATH=src python -m lbcc.cli compact tests/fixtures/sample_bundle.json \
  --max-bytes 5000 --max-loss-ppm 350000 > result.json

PYTHONPATH=src python -m lbcc.cli verify tests/fixtures/sample_bundle.json result.json
```

## Status semantics

- `PASS`: a capsule was produced within byte and loss policy.
- `FREEZE`: producing a capsule would violate an invariant or security/quality constraint.

This local protocol maps naturally onto NEXY's wider freeze-oriented control philosophy, but remains an independent proposal until explicitly integrated.

## Repository boundary

This project writes only to `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/...`. It does not modify NEXY.AI source code.
