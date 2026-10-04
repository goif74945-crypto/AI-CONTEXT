# NEXY Workstream Orthogonality & Collision Firewall (WOCF)

**Classification:** EXPERIMENTAL / AI-PROPOSED / standalone reference lab  
**Repository target:** `goif74945-crypto/AI-CONTEXT` only  
**NEXY.AI repository mutation:** forbidden and not performed

WOCF is a deterministic preflight layer for concurrent AI/agent workstreams. It answers one narrow question before a workstream begins durable mutation:

> Does this proposed workstream collide with existing work by identity, namespace, write-set, exclusive resource, or excessive lexical concept overlap?

It does **not** authorize execution, allocate workers, verify product truth, schedule jobs, or modify NEXY policy.

## Core decisions

- `ALLOW` — no collision or material overlap detected under the supplied catalog/policy.
- `WARN` — material lexical overlap exists but no hard collision was found.
- `FREEZE` — fail closed because a hard collision, protected target, malformed input, or high-overlap condition was detected.

## Determinism

The reference implementation uses only Python standard-library logic: normalized manifests, exact path overlap, exact exclusive-resource comparison, SHA-256 canonical fingerprints, and deterministic lexical Jaccard scoring. No embedding model, external LLM, network call, or hidden model judgment is used in the decision path.

## Quick verification

```bash
python scripts/run_verification.py
```

The final validation report records the exact observed gate results for the committed source.

## Important limitation

Lexical overlap is **not semantic truth**. Different wording can hide duplicate concepts and similar wording can describe distinct work. Therefore WOCF is a preflight guard, not a canonical novelty oracle.
