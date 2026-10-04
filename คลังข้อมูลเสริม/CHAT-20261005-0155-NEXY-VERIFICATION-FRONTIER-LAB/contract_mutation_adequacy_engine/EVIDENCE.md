# Contract Mutation Adequacy Engine — Evidence

**Local status:** PASS

## Executed proof

- E2: `contract_mutation_adequacy_engine.test_engine` — 5 focused tests after defect repair.
- E2 adversarial: `max_mutants` cap is exact and deterministic.
- Regression evidence: non-positive mutation budgets now fail explicitly after re-audit found the configuration defect.
- Determinism replay: full 33-test suite passed under two hash seeds.

## Defect found and repaired

During re-audit, `max_mutants=0` could previously admit one generated mutant before stopping and could support misleading vacuous configuration semantics. The implementation now rejects non-positive/non-integer mutation budgets and the regression test passes.

## Claims proven

Tests establish deterministic unique mutant generation, weak-oracle survivor detection, strict-oracle complete kills for the generated operator set, baseline precondition enforcement, budget validation, and deterministic capping.

## Evidence boundary

These results prove the standalone reference implementation in this lab at E1/E2 and the stated lab-level E3 interactions. They do **not** prove integration into NEXY.AI, production performance, deployment readiness, or authority promotion.
