# Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R1 | Five distinct Lo4 proposals | five component designs/modules | repository files + tests | PASS |
| R2 | Proposal cannot self-promote to Canon | SIMF status + integration advisory | integration tests | PASS |
| R3 | Dangerous authority expansion freezes | `cawt.py` | unit + integration negative control | PASS |
| R4 | Stale/insufficient evidence creates debt | `edel.py` | unit + integration negative control | PASS |
| R5 | Dependent claims inherit proof debt | `edel.py` | propagation test | PASS |
| R6 | Evidence dependency cycles reject | `edel.py` | cycle negative test | PASS |
| R7 | Emergent privilege composition freezes | `ccf.py` | unit + integration negative control | PASS |
| R8 | Scope exclusions prevent unauthorized composition | `ccf.py` | scope-lock test | PASS |
| R9 | Invariants remain proposal-only and falsifiable | `simf.py` | mining/falsification tests | PASS |
| R10 | Replay detects divergent outputs and executor faults | `drcdo.py` | differential tests | PASS |
| R11 | One executor cannot poison a later replay | `drcdo.py` deep canonical copy | mutation isolation test | PASS |
| R12 | Canonical output order-independent where promised | common canonicalization + sorted inputs | permutation tests + 40k stress | PASS |
| R13 | Cross-system gate freezes on any critical blocker | `integration.py` | integration test | PASS |
| R14 | NEXY runtime integration works | none attempted | requires exact NEXY target + E3/E4+ | NOT_VERIFIED |
| R15 | Production/deployment ready | none attempted | requires E5/E6 | NOT_VERIFIED |
