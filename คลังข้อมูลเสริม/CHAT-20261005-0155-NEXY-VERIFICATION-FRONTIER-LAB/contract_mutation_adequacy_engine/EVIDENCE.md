# Contract Mutation Adequacy Engine — Evidence

**Local status:** PASS

## Executed proof

- E2: `contract_mutation_adequacy_engine.test_engine` — 6 focused tests after defect repair.
- E2 adversarial: `max_mutants` cap is exact and deterministic.
- Regression evidence: non-positive mutation budgets now fail explicitly, and zero-mutant contracts cannot produce a vacuous `1.0` adequacy score.
- Determinism replay: full 34-test suite passed under two hash seeds.

## Defect found and repaired

During re-audit, two related adequacy defects were found: (1) `max_mutants=0` could admit one generated mutant before stopping, and (2) a contract with no generated mutants could produce a vacuous `score=1.0`. The implementation now rejects non-positive/non-integer mutation budgets and rejects adequacy evaluation when no mutants are generated. Both regression tests pass.

## Claims proven

Tests establish deterministic unique mutant generation, weak-oracle survivor detection, strict-oracle complete kills for the generated operator set, baseline precondition enforcement, budget validation, zero-mutant fail-closed behavior, and deterministic capping.

## Evidence boundary

These results prove the standalone reference implementation in this lab at E1/E2 and the stated lab-level E3 interactions. They do **not** prove integration into NEXY.AI, production performance, deployment readiness, or authority promotion.
