# Design — Lo4 Mutation Tournament (LMT)

**Status:** Lo4 EXPERIMENTAL / intentionally incapable of Canon promotion.

## Objective
Allow aggressive AI-proposed ideas to compete without allowing novelty pressure to bypass invariants or authority.

## Candidate metrics
Exactly five normalized metrics in `[0,1]`: `safety`, `utility`, `proof`, `reversibility`, `novelty`.

## Gates
1. Any invariant failure -> reject.
2. Threshold failure -> reject. Defaults: safety >= 0.90, proof >= 0.80, reversibility >= 0.60.
3. Eligible candidates are Pareto-filtered across all five metrics.
4. A deterministic weighted score selects one recommendation from the frontier, ID as final tie-break.

## Absolute authority lock
Every returned result contains:
- `promotion_permitted: false`
- `authority: EXPERIMENTAL_ONLY`

This is a deliberate structural property: “winning” means only “candidate recommended for further proof.”

## NEXY value
Creates a controlled space for extreme Lo4 innovation without confusing creative search with governance. Metric provenance/truth remains an upstream obligation.
