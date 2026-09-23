# NEXY.AI Concurrency Model

## Purpose
Central map of race/order/parallelism/idempotency semantics across NEXY domains.

## Critical rule
NEXY does **not** have one global concurrency policy:
- current DOC-C pipeline allows concurrent multi-agent/pipeline work under queue bounds;
- future constitutional Core requires one canonical mutator;
- game-authoritative simulation uses deterministic tick/order rules;
- robotics separates fast and safe loops.

Do not copy a concurrency rule across domains without authority.

## Files
- `concurrency-model.json`
- `validation-report.md`
