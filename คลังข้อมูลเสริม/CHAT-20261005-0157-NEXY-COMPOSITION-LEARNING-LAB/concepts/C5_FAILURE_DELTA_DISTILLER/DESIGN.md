# C5 — Failure Delta Distiller (FDD)

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## Objective
Reduce a long failing sequence to a deterministic **1-minimal** subsequence that still reproduces the same stable failure signature.

## Algorithm
- classic delta debugging (`ddmin`) over ordered subsequences;
- deterministic chunk traversal;
- final single-element removal pass to establish 1-minimality;
- every oracle evaluation is repeated twice;
- if the same candidate returns different signatures, freeze with `ORACLE_NONDETERMINISTIC`;
- if the original input does not reproduce target signature, freeze.

## Truthful minimality contract
`1-minimal` means removing any one remaining item stops reproducing the target. It does **not** claim global minimum cardinality. The distinction is explicit because a convenient but false “smallest possible” claim would violate evidence discipline.

## Cost tradeoff
Double oracle confirmation intentionally increases oracle calls to guard against flaky minimization. For expensive production oracles, future work may use statistically stronger/cheaper stability policies, cached immutable receipts, or deterministic replay IDs.

## Why NEXY could benefit
A multi-agent/tool failure can involve dozens or hundreds of steps. A small stable reproducer improves debugging, incident review, regression test creation, and evidence review. C2 already demonstrates one integration: an emergent risk finding becomes the target signature that C5 minimizes.

## Code / tests
- Code: `src/nexy_aux/distiller.py`
- Integration: `src/nexy_aux/integration.py`
- Tests: `tests/test_distiller.py`, `tests/test_integration.py`, `tests/test_properties.py`, `tests/test_hardening.py`
