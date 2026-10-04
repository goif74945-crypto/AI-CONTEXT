# 04 — Shadow Invariant Miner & Falsifier (SIMF)

**Class:** `Lo4_AI_PROPOSAL_ONLY`

## Purpose
Use successful execution observations to discover patterns that *might* be invariants, then attempt to falsify them. The crucial property is governance: mined patterns are never promoted automatically.

## Candidate classes
Reference implementation mines:
- CONSTANT(field=value)
- NUMERIC_RANGE(field in observed min..max)
- FIELD_EQUALITY(left==right)

Every candidate carries `Lo4_AI_PROPOSAL_ONLY` regardless of support count.

## Falsification
Challenge observations are evaluated against each candidate. The first deterministic counterexample records the candidate and observation. Surviving candidates remain proposals, not Canon.

## Why this matters
Passing systems often contain undocumented assumptions. Mining can expose those assumptions to human/system review without committing the classic error “observed often” = “law”.

## Invariants
- at least two observations required;
- proposal status cannot be replaced by the miner;
- challenge counterexample removes candidate from survivors;
- survival never equals promotion.

## Complexity
Constant/range mining is O(observations × fields). Pairwise equality mining is O(observations × fields²). Intended for bounded structured trace schemas.

## Code/Test
- code: `src/nexy_lo4_frontier/simf.py`
- tests: `tests/test_simf.py`
