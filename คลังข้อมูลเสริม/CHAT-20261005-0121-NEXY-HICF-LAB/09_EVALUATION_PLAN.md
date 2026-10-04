# 09 — EVALUATION PLAN

## E1 static checks

- Python files compile.
- JSON schema documents parse as JSON.
- deterministic fingerprint is stable across set-like ordering.

## E2 unit behavior

Required tests:
- non-material unknown + safe reversible read-only action → PROCEED;
- material unknown → ASK;
- critical unknown → FREEZE;
- authority conflict → FREEZE;
- prohibited capability → FREEZE;
- unresolved authority + high-impact mutation → ASK;
- friction budget cannot suppress required ASK;
- repeated question detection;
- durable inferred preference rejected;
- immutable drift → AUTHORITY_BREAK;
- objective drift → MATERIAL;
- output record JSON serializable;
- invalid empty objective rejected.

## Exhaustive model matrix

Cross product:
- 3 authority states;
- 4 unknown states (none + three materialities);
- 4 impact levels;
- 3 reversibility states;
- 2 mutation states;
- 2 prohibition states.

Total: `3 × 4 × 4 × 3 × 2 × 2 = 576` cases.

Invariant assertions include:
- authority conflict always freezes;
- explicit prohibition freezes unless an earlier authority conflict already freezes for another reason;
- critical unknown freezes under resolved authority when not otherwise prohibited;
- material unknown asks under resolved authority;
- fully resolved/no-unknown/resolved-authority/non-prohibited input proceeds.

## Future evaluation

- transcript replay benchmark;
- multi-model consistency evaluation;
- user correction rate;
- stale-context injection;
- adversarial preference poisoning;
- clarification batching quality;
- long-horizon resume after checkpoint compaction;
- multilingual intent equivalence.
