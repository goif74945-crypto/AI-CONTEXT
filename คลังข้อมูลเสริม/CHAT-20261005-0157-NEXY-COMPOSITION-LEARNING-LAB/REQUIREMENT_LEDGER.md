# Requirement Ledger

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| R01 | Five distinct AI-proposed concepts exist | Design inventory | PASS |
| R02 | No NEXY.AI mutation is required by implementation | Architecture inspection | PASS |
| R03 | Deterministic serialization/fingerprints | unit/property tests | PASS |
| R04 | C1 freezes on unsatisfied/contradictory contracts | `test_composition.py` | PASS |
| R05 | C2 detects hazardous composed dataflows | `test_emergence.py`, property tests | PASS |
| R06 | C3 never substitutes evidence class and obeys explicit transfer policy | `test_portability.py`, property tests | PASS |
| R07 | C4 prevents silent scope expansion and tests regression assertions | `test_corrections.py`, property tests | PASS |
| R08 | C5 reproduces target signature and returns a 1-minimal subsequence | `test_distiller.py`, property tests | PASS |
| R09 | Cross-concept Risk→Distill composition works | `test_integration.py` | PASS |
| R10 | CLI surfaces deterministic machine-readable execution | `test_cli.py` | PASS |
| R11 | Python static bytecode compilation succeeds | compileall | PASS |
| R12 | Persisted GitHub artifacts are read-back verified | pending GitHub write/read-back | NOT_VERIFIED |

Status is intentionally not mission-COMPLETE until R12 is proven.
