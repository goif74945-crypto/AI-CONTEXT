# Verification Report — EPC Mutation Adversary Laboratory 20

## Standalone E1/E2 result
- Python compileall: PASS.
- Static AST decision-package audit: PASS; 9 package files; no forbidden `random`, `time`, or `secrets` imports.
- Unit/adversarial suite: PASS; 39 tests.
- Pairwise mutant combinations: 190 pairs exercised.
- All twenty combined: every expected invariant preserved/detected.
- Mutation campaign: PASS; 20 killed / 20; 0 escaped.
- Mutation score Q64.64 raw: `18446744073709551616` (exact 1.0).
- Baseline digest: `2048f73637aae394d845fa5ab3a86dbb40e56f5ce2a0badab8ac81177505f99a`.
- Campaign report digest: `7a9c25710d6aebcb8ad35c09dfd8b0bd4d6ba8ad0c1d44b389b29ce60ddb1127`.
- Independent report verifier: PASS.

## Failure / repair evidence
Initial full verification had one failure involving composition of `M06_WIP_AS_CUT_EVIDENCE` and `M07_VOTE_BUDGET_DOUBLE_SPEND`.

Root cause: M07 overwrote `requested_round`, erasing M06's intended WIP/CUT violation.

Repair: M07 now consumes another vote right for the already-active round without rewriting the round. The complete compile/static/unit/adversarial/campaign pipeline was rerun and passed.

## Evidence boundary
These results prove the standalone tested artifact only. Actual NEXY integration, runtime, deployment, release, and Canon promotion remain `NOT_VERIFIED`.
