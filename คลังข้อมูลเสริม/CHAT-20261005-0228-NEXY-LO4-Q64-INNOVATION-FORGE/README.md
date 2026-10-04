# NEXY Lo4 Q64 Innovation Forge

**Classification: `AI_PROPOSED_LO4_ONLY / NON_CANONICAL / STANDALONE_REFERENCE_IMPLEMENTATION`.**

This laboratory explores twenty quantitative control mechanisms that could become useful to future NEXY.AI work only after formal review and promotion. It deliberately does **not** modify NEXY.AI, redefine NEXY law, or claim production integration.

The common substrate is signed **Q64.64** fixed-point arithmetic represented by JavaScript `BigInt`, constrained to a signed 128-bit raw range. Domain quantities are accepted as decimal strings, not binary floating-point values. Core arithmetic uses checked range enforcement and round-to-nearest-even.

## Why this exists
NEXY's current context emphasizes deterministic execution, evidence-first decisions, explicit authority, freeze-on-ambiguity, external AI as workers rather than authority, and controlled evolution. This project tests a complementary idea: many future decision-support mechanisms can share one narrow, deterministic quantitative protocol instead of each inventing its own scoring arithmetic.

## What is implemented
Twenty independently callable concepts are registered behind `runConcept(id, payload)`. Every module is marked `AI_PROPOSED_LO4_ONLY`, has deterministic failure semantics, and returns `PASS`, `FREEZE`, or where applicable `REJECT` without obtaining release authority.

The CLI accepts a JSON envelope containing a concept ID and payload and emits canonical JSON plus a SHA-256 result digest. Same normalized input and implementation must yield byte-stable structural output.

## Verification snapshot
The exact authored source was locally verified with:
- syntax/static checks;
- 107 Node tests;
- 16 independent Python exact-rational Q64 oracle vectors;
- 10,000 deterministic replay executions across all 20 concepts;
- 20,000-evaluation benchmark workload;
- CLI smoke execution.

These are standalone E1/E2/E3-local claims. They are **not** E4-E7 evidence for NEXY.AI.

## Quick run
```bash
npm run test:all
python3 scripts/q64-oracle.py
node scripts/replay-stress.mjs
node bench/benchmark.mjs
node src/cli.js fixtures/smoke.json
```

## Integration boundary
Future NEXY code, if explicitly authorized, should call this kind of engine through a narrow adapter and consume only structured deterministic results. NEXY LAW/JUDGE/Safety authority must remain outside the module. See `05_NEXY_INTEGRATION_CONTRACT.md`.
