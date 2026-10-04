# Requirement Ledger

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| R01 | additive-only mission folder | repository path audit | PASS |
| R02 | zero mutation to NEXY.AI-named repositories | mutation target audit | PASS |
| R03 | explicit lifecycle and bounded lease | source + unit tests | PASS |
| R04 | FILE/TREE structural write collision | unit + stress tests | PASS |
| R05 | protected-scope collision | unit test | PASS |
| R06 | exclusive-resource collision | unit test | PASS |
| R07 | exclusive-authority collision | unit test | PASS |
| R08 | declared overlap only; no hidden embedding authority | architecture + source inspection | PASS |
| R09 | missing critical declarations reject | unit tests | PASS |
| R10 | explicit timezone-aware clock | unit test | PASS |
| R11 | inactive/expired incumbents ignored | unit tests | PASS |
| R12 | registry-order invariance | unit + stress tests | PASS |
| R13 | controlled-tag NFKC/casefold normalization | unit test | PASS |
| R14 | severity lattice PROCEED < COEXIST < DECONFLICT < FREEZE | source + tests | PASS |
| R15 | full-state SHA-256 decision seal | source + hash invariance/change tests | PASS |
| R16 | duplicate incumbent mission IDs fail closed | unit test | PASS |
| R17 | adversarial fixture corpus includes high-overlap distinct-path case | fixture replay | PASS |
| R18 | exact repository bytes verified before completion | 4/4 Git blob SHA matches + exact execution | PASS |

Truth boundary: PASS applies to the standalone reference prototype at E1/E2 only. It does not establish NEXY runtime integration or deployment behavior.