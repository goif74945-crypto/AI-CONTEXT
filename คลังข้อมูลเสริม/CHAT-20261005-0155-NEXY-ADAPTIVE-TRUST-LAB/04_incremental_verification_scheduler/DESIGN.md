# IVS — Incremental Verification Scheduler

**Status:** AI_PROPOSAL / NON_GOVERNING

## Objective
Turn change impact into the smallest *reasonable* deterministic verification rerun plan without treating stale evidence as current. This is a scheduling layer, not a proof that the selected tests are complete.

## Separation from evidence invalidation
Existing invalidation work defines when proof expires. IVS consumes a dependency graph plus test coverage metadata after a change and schedules affected verification. The reference uses a deterministic cost-aware greedy set-cover heuristic and never claims global optimality.

## Model
- dependency graph maps node → direct dependencies;
- changed nodes propagate to all dependents;
- each test declares nodes it covers and a positive cost;
- scheduler greedily selects the test with highest uncovered-impact-per-cost, deterministic tie-break by test name.

## Invariants
- changed node is always impacted;
- transitive dependents are impacted;
- tests with invalid cost/empty name freeze planning;
- if any impacted node has no test coverage, status is `FREEZE` and uncovered nodes are explicit;
- successful `PLAN` proves only selection logic, not that tests themselves pass.

## Integration
Run after a verified change diff/dependency map is available and before actual test execution. Results should feed the existing evidence ledger after tests run.
