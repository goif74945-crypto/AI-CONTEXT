# Evidence Ledger

Target: isolated Q64 Constitutional Physics reference implementation.
Environment: local Python 3.13 runtime in the current execution container.
Authority: Lo4 proposal only.

| ID | Claim | Class | Artifact | Status |
|---|---|---|---|---|
| EV-RED-001 | tests were authored before package implementation and failed for missing `qcp` | E2/TDD | `TDD_RED.txt` | PASS |
| EV-FIX-001 | first implementation exposed Q64 1-ULP conservation defect | E2 | `TDD_GREEN_INITIAL.txt` | PASS as defect evidence |
| EV-FIX-002 | corrected implementation passes target regression | E2 | `ULP_REGRESSION_GREEN.txt` | PASS |
| EV-FIX-003 | reverting correction reproduces regression | E2 | `ULP_REGRESSION_RED.txt` | PASS as red proof |
| EV-UNIT-001 | full expanded unit/adversarial/integration suite | E2/E3 isolated | `FINAL_TESTS.txt` | PASS, 37/37 |
| EV-STRESS-001 | deterministic/property checks | E2 | `STRESS.txt` | PASS, 1000 |
| EV-STATIC-001 | package/tests compile | E1 | `STATIC_COMPILE.txt` | PASS |
| EV-Q64-001 | executable package contains no Python float constants | E1 | `NO_FLOAT_AST.txt` | PASS, 0 float constants |

## Claim boundaries
E1/E2/E3 above prove only the isolated bytes referenced by the final hash manifest. They do not prove production integration, deployment, distributed concurrency, security penetration resistance, or Canon promotion.
