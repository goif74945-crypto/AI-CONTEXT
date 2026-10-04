# NEXY Deterministic Interchange Kernel (NDIK)

**Status:** AI-proposed standalone research/reference implementation. It is **not** a canonical NEXY requirement and is **not** integrated into the NEXY.AI implementation repository.

## Why this exists

NEXY's context requires deterministic behavior, provenance-aware evidence, explicit state, replay safety, idempotent critical writes, and zero-guess failure behavior. Those properties become fragile when the same logical payload is serialized differently by different runtimes, object-key orders, Unicode forms, numeric semantics, or hidden clock/random inputs.

NDIK isolates that boundary. It turns a strict JSON-compatible value into a deterministic UTF-8 representation and a domain-separated SHA-256 fingerprint, then optionally wraps it in a deterministic proof-carrying envelope.

## Key properties

- deterministic object ordering;
- NFC normalization for strings and keys;
- normalization-collision rejection;
- duplicate JSON key rejection during strict parsing;
- floats rejected rather than silently rounded;
- default integer bounds limited to the exact JavaScript-safe range;
- cycles rejected;
- bounded depth, node count, and output bytes;
- no implicit time, randomness, environment, network, or global mutable state;
- domain-separated SHA-256 fingerprints;
- tamper-detecting envelope hash plus payload hash;
- strict envelope field set to prevent silent extension drift.

## Intended future integration points

This reference can later be adapted for NEXY boundaries such as Vault object identity, evidence artifacts, idempotency keys, replay capsules, provider/tool inputs, audit references, cache keys, and cross-language compatibility tests. Integration requires a separate authorized change to the NEXY.AI repository and cross-runtime conformance work.

## Explicit non-goals

- not a cryptographic signature system;
- not authorization;
- not encryption;
- not RFC 8785 compliance claim;
- not a replacement for schema validation;
- not proof of production integration;
- not permission to modify NEXY.AI.

## Run locally

```bash
python -m pytest
PYTHONPATH=src python examples/demo.py
```

See `03_ARCHITECTURE.md`, `04_REQUIREMENT_LEDGER.md`, and `EVIDENCE/` for the design and verification record.
