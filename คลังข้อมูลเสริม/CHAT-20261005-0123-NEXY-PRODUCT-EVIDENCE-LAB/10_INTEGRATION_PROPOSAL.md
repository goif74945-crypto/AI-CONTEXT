# 10 — Non-Governing Integration Proposal

`AI-PROPOSED` only. No implementation claim.

A future NEXY integration could place NPEL-like logic behind a product/research workflow rather than inside the deterministic execution core.

Potential boundary:

```text
Human product intent
  → proposal form
  → NPEL compiler
  → immutable experiment contract hash
  → external experimentation platform
  → evidence adapter
  → NPEL evaluator
  → evidence state shown in NEXY::VIEW
  → human decision
```

## Why outside CORE

Product experimentation uses statistical assumptions and domain tradeoffs that should not silently become core law. The deterministic part is contract validation and evidence classification under explicitly chosen assumptions, not an assertion that those assumptions are universally correct.

## Promotion gate

Before any production promotion, a separate authoritative specification would need to define:
- supported statistical designs;
- sequential-testing policy;
- privacy/consent policy;
- event provenance and retention;
- segment safety rules;
- role/access boundaries;
- audit retention;
- integration tests against the actual analytics/experiment provider;
- product authority for starting/stopping experiments.
