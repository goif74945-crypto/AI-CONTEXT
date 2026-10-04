# Verification Portfolio Optimizer — Evidence

**Local status:** PASS

## Executed proof

- E2: `verification_portfolio_optimizer.test_engine` — 6 focused unit/negative tests.
- E2 adversarial: equal-cost alternatives prefer fewer checks deterministically.
- E3 lab integration: NSCA missing negative proof → VPO chooses qualifying E2 check and rejects cheaper E1 substitution.
- Determinism replay: full 33-test suite passed under two hash seeds with byte-identical result bodies.

## Claims proven

Tests establish exact minimum-cost behavior for supplied fixtures, deterministic tie-breaks, explicit evidence-class matching, invalid input rejection, zero-claim behavior, and exact-state-space bound enforcement.

## Evidence boundary

These results prove the standalone reference implementation in this lab at E1/E2 and the stated lab-level E3 interactions. They do **not** prove integration into NEXY.AI, production performance, deployment readiness, or authority promotion.
