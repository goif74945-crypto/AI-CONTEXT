# Requirement Ledger

| ID | Requirement | Evidence target | Status before durable upload |
|---|---|---|---|
| R-01 | Five divergent Lo4 concepts | directory inventory | PASS locally |
| R-02 | Minimal-Cut Failure Geometry implemented | engine + tests | PASS locally |
| R-03 | Liveness / Deadlock Sentinel implemented | engine + tests | PASS locally |
| R-04 | Dependency Dominator Analyzer implemented | engine + tests | PASS locally |
| R-05 | Symmetry State-Space Reducer implemented | engine + tests | PASS locally |
| R-06 | Lo4 Mutation Tournament implemented | engine + tests | PASS locally |
| R-07 | All remain non-Canon EXPERIMENTAL | docs + tournament lock | PASS locally |
| R-08 | TDD RED observed before implementation | `RED_TEST.txt` | PASS |
| R-09 | Full unit/property verification | validation outputs | PASS locally |
| R-10 | Static compilation | compile evidence | NOT_VERIFIED until final validation |
| R-11 | No NEXY.AI repo mutation | mutation target ledger | PASS by executed action scope so far |
| R-12 | Durable write to AI-CONTEXT | GitHub receipts | NOT_VERIFIED until upload |
| R-13 | Read-back verification | GitHub fetch after upload | NOT_VERIFIED until upload |
| R-14 | Exact hash manifest | SHA-256 manifest | NOT_VERIFIED until final local seal |

`PASS locally` proves only this reference artifact in the local execution environment, not NEXY.AI integration/runtime/deployment.
