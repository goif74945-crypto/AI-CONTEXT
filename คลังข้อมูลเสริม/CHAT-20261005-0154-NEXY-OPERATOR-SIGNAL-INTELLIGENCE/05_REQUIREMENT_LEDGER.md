# Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R01 | Deterministic canonical identity | `canonical.py` | determinism + tests | PASS |
| R02 | FREEZE/SECURITY non-suppressible | `salience.py`,`routing.py` | unit tests | PASS |
| R03 | Quiet mode only silences routine LOW | `routing.py` | unit tests | PASS |
| R04 | Ack-required signals stay visible | `routing.py` | unit test | PASS |
| R05 | Repetitive progress compression | `compress.py` | unit tests | PASS |
| R06 | Preserve state/evidence/user-critical milestones | `compress.py` | unit tests | PASS |
| R07 | Canonical nested/list outcome diff | `delta.py` | unit tests | PASS |
| R08 | UNKNOWN remains UNKNOWN | `delta.py` | unit tests | PASS |
| R09 | JSON Pointer redaction incl. root | `delta.py` | regression tests | PASS |
| R10 | Explicit logical acknowledgement debt | `debt.py` | unit tests | PASS |
| R11 | High/critical unresolved debt blocks all_clear | `debt.py` | unit tests | PASS |
| R12 | Invalid/future ack fails closed | `debt.py` | negative tests | PASS |
| R13 | Machine-readable five-command CLI | `cli.py` | subprocess tests | PASS |
| R14 | No production network/subprocess/eval/exec/open | source package | AST static scan | PASS |
| R15 | NEXY production integration | outside lab | no executed integration | NOT_VERIFIED |
