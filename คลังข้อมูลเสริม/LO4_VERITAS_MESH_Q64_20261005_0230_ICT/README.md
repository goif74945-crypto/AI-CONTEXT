# Lo4 VERITAS MESH — Q64.64 Experimental Promotion Laboratory

**Work ID:** `NEXY-LO4-VERITAS-MESH-20261005-0230-ICT`  
**Authority:** `PROPOSAL / Lo4 / NON-CANONICAL`  
**Target:** NEXY.AI compatibility research and reusable implementation  
**Mutation boundary:** NEXY.AI repository is read-only; this work lives only in AI-CONTEXT.

## What this is

VERITAS MESH is an executable Lo4 evaluation fabric for candidate capabilities before any formal promotion into NEXY Canon. It turns fuzzy statements such as “this feature looks safe/useful/tested” into a deterministic vector of 20 bounded Q64.64 scores, then applies fail-closed promotion gates.

It **does not** change Canon, cannot promote itself, and never claims that an experimental score is authoritative truth. Its output can only be:

- `REJECT`
- `QUARANTINE`
- `ELIGIBLE_FOR_PROMOTION_REVIEW`

There is intentionally no `PROMOTED` state.

## Why it is distinct from the existing six knowledge packs

The existing `คลังข้อมูลเสริม` files are advisory architecture/research notes about evidence, context, security, failures, evals, and research backlog. VERITAS MESH is different in kind: it is a runnable Q64.64 decision laboratory with a fixed signal schema, 20 executable scoring models, deterministic receipts, critical rejection gates, property-style stress tests, and benchmark evidence.

Some inputs deliberately consume concerns already present in prior research, such as evidence quality or regression risk. That is dependency reuse, not a claim that those concerns were invented here. The new contribution is the deterministic Lo4 composition and promotion-control mechanism.

## Quick run

```bash
npm test
npm run bench
tsc -p tsconfig.json --pretty false
```

No third-party runtime dependency is required. Node.js built-ins are sufficient.

## Core invariants

1. Every scoring signal is `UnitQ64`, constrained to `[0, 1]`.
2. Raw wire representation is signed Q64.64: `raw / 2^64`.
3. Scoring accepts no JavaScript `number` path.
4. Multiplication/division use `bigint` exact intermediates.
5. Division by zero fails closed.
6. A catastrophic weak critical gate forces `REJECT` even if the average looks good.
7. A strong candidate is only eligible for human/authorized promotion review.
8. `canonicalPromotionPerformed` is hard-coded to `false` in the decision contract.
9. Portable output serializes Q64.64 raw values as decimal strings to avoid JSON number precision loss.
10. NEXY.AI is never mutated by this project.

## Status

Standalone implementation evidence in `evidence/` currently proves E1 static and E2 unit/stress behavior for this isolated project. It does **not** prove integration inside NEXY.AI, deployment, production performance, or canonical acceptance.

## Chat reference

Internal ChatGPT conversation ID is **UNKNOWN** because the runtime does not expose it to the assistant. To avoid inventing an identifier, this work uses the durable Work ID `NEXY-LO4-VERITAS-MESH-20261005-0230-ICT`.
