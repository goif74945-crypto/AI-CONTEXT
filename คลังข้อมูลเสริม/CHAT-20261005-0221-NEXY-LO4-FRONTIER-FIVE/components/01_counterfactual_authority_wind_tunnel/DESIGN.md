# 01 — Counterfactual Authority Wind Tunnel (CAWT)

**Class:** `Lo4_AI_PROPOSAL_ONLY`

## Purpose
Before adopting a new authority/policy set, replay a deterministic corpus of decisions under both baseline and candidate rules. Expose the exact cases where the candidate changes authority, especially DENY→ALLOW, FREEZE→ALLOW, or new same-priority conflicts.

## Why this is distinct
Ordinary policy validation asks whether a policy is syntactically/structurally valid. CAWT asks a different question: **what authority behavior changes if this candidate replaces the baseline?**

## Inputs
- baseline `AuthorityRule[]`;
- candidate `AuthorityRule[]`;
- `DecisionCase[]` containing action/resource/attributes.

## Deterministic semantics
Rules are canonicalized. Matching uses explicit action/resource patterns plus required attributes. Only highest-priority matches decide. Opposite effects at the same top priority freeze. No match freezes.

## Divergence severity
- AUTHORITY_EXPANSION: 5
- CONFLICT_INTRODUCED: 4
- FREEZE_REMOVED_TO_ALLOW: 4
- AVAILABILITY_REGRESSION: 3
- FREEZE_INTRODUCED: 2
- other structural divergence: 1

Severity >= 4 freezes the wind-tunnel report.

## Invariants
- baseline is never mutated;
- every decision is reproducible from canonical inputs;
- same-priority ALLOW/DENY conflict cannot be silently tie-broken;
- minimal witness is deterministic: highest severity then lexical case id.

## Complexity
Roughly O(cases × rules) for the reference evaluator. It favors inspectability and deterministic behavior over speculative indexing. Production-scale adoption could compile pattern indexes while preserving output equivalence.

## Failure model
Malformed rule/case → structural exception. No matching authority → decision FREEZE. Dangerous candidate divergence → report FREEZE.

## Code/Test
- code: `src/nexy_lo4_frontier/cawt.py`
- tests: `tests/test_cawt.py`, permutation stress in `tests/test_determinism_properties.py`
