# Requirement Ledger

| ID | Requirement | Implementation | Evidence target | Status |
|---|---|---|---|---|
| MVK-R01 | Standalone and does not import NEXY.AI | package boundary | E1 import/compile | PASS |
| MVK-R02 | Immutable public case/observation mappings | `model.py` | E2 defensive-copy test | PASS |
| MVK-R03 | Deterministic canonical hashing | `canonical.py` | E2 order/hash tests | PASS |
| MVK-R04 | Reject nondeterministic unsupported values | `canonical.py` | E2 negative tests | PASS |
| MVK-R05 | Execute baseline + derived relation | `engine.py` | E2 engine tests | PASS |
| MVK-R06 | Adapter/mutator/oracle errors fail closed | `engine.py` | E2 error-path tests | PASS |
| MVK-R07 | Detect irrelevant-context drift | `relations.py` | E2 pass/fail tests | PASS |
| MVK-R08 | Detect deterministic replay drift | `relations.py` | E2 stateful adapter test | PASS |
| MVK-R09 | Permission reduction cannot increase effects/authority | `relations.py` | E2 negative tests | PASS |
| MVK-R10 | Evidence removal cannot increase effects/authority | `relations.py` | E2 negative tests | PASS |
| MVK-R11 | Semantic variants supported without claiming automatic equivalence | `relations.py` | E2 test + design boundary | PASS |
| MVK-R12 | Local CLI fixture validation | `cli.py` | local entrypoint execution | PASS |
| MVK-R13 | Real NEXY integration | future adapter | E3 against exact NEXY revision | NOT_VERIFIED |
| MVK-R14 | Production/runtime/deployment behavior | future | E5/E6 | NOT_VERIFIED |
