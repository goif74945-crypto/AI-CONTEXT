# NEXY Deterministic Interleaving Verifier Lab

**Classification:** AI-PROPOSED / AUXILIARY / NON-CANONICAL  
**Execution reference:** `CHAT-20261005-0144-NEXY-INTERLEAVING-VERIFIER`

This lab is a standalone reference verifier stored in `AI-CONTEXT`. It does **not** modify NEXY.AI and does not claim to be part of current NEXY implementation.

## Purpose
Parallel agents/actions are useful until two legal schedules produce two different authoritative states. This tool models a bounded plan as deterministic atomic actions and explores the exact reachable state space.

It answers:
1. Can every mandatory action execute under every reachable ordering allowed by dependencies?
2. Does any reachable post-action state violate a declared invariant?
3. Do all complete legal schedules converge to the same canonical terminal state?
4. Which unordered actions have overlapping read/write footprints?
5. If divergence exists, what two reproducible schedules witness it?

## Decision law
- `PASS + CONFLUENT`: complete bounded state space explored, all mandatory transitions legal, invariants preserved, exactly one terminal state.
- `FAIL`: one concrete counterexample proves precondition failure, execution-model failure, invariant violation, or divergent terminal states.
- `NOT_VERIFIED + FREEZE_*`: the model is invalid or the exact exploration budget was exhausted. Partial exploration never becomes PASS.

## Why state merging is exact
A search node is identified by `(completed action IDs, canonical state)`.
If two schedules reach the same node key, all future enabled actions and all future deterministic transition results are identical because dependencies depend only on the completed set and action semantics depend only on the current state. Merging those histories therefore removes duplicate work without removing reachable future behavior.

## Safe action DSL
Predicates: `exists`, `not_exists`, `eq`, `neq`, `int_range`, `unique`.
Effects: `set`, `add`, `copy`, `delete`, `append_unique`.

No `eval`, code loading, shell, network, environment, clock, randomness, or arbitrary callbacks exist in the core.
Floating point is intentionally rejected; adapters should use scaled integers/fixed-point when decimals matter.

## Quick run
```bash
PYTHONPATH=src python -m interleaving_verifier fixtures/confluent.json --pretty
PYTHONPATH=src python -m interleaving_verifier fixtures/divergent.json --pretty
```

Exit codes:
- `0`: PASS / CONFLUENT
- `2`: decisive FAIL counterexample
- `3`: file/JSON/output I/O failure
- `4`: NOT_VERIFIED / FREEZE

## Verification
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src tests
```

See `VERIFY.md` and `FINAL_AUDIT.md` for exact evidence once sealed.
