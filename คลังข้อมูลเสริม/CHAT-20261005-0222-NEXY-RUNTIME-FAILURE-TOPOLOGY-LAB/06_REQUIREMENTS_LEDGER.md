# Requirements Ledger

| ID | Requirement | Implementation | Evidence | Current local status |
|---|---|---|---|---|
| R01 | Five materially distinct runtime-failure systems | five source modules + design pack | collision audit + tests | PASS |
| R02 | Deadlock detects self/multi-node/disjoint cycles and ignores acyclic chains | `deadlock.py` | deadlock unit/adversarial tests | PASS E2 |
| R03 | Deadlock analysis must be stack-safe for long valid chains | iterative SCC | 1,500-node regression + scaling probe | PASS E2 / observational perf |
| R04 | Livelock distinguishes progress, stall, cycle, corrupt progress history | `livelock.py` | focused + transient-prefix regression tests | PASS E2 |
| R05 | Retry never mints idempotency/retryability | `retry.py` | non-idempotent/non-retryable/history laundering tests | PASS E2 |
| R06 | Retry storms use trailing signature streak and bounded backoff | `retry.py` | streak reset, threshold, cap tests | PASS E2 |
| R07 | Poison identity is input+revision+failure scoped | `quarantine.py` | revision/input/signature/success reset tests | PASS E2 |
| R08 | Salvage requires verified/evidenced/user-safe dependency closure | `salvage.py` | DAG, cycle, branch, dependency tests | PASS E2 |
| R09 | Salvage cannot claim whole-task completion | `salvage.py` hard false boundary | authority-regression RED/GREEN evidence | PASS E2 |
| R10 | Semantically unordered inputs produce deterministic reports | canonical normalization | permutation tests | PASS E2 |
| R11 | Production source has no forbidden effectful I/O boundary | pure library + static verifier | `scripts/verify.py` | PASS E1 |
| R12 | All five compose in one failure scenario | integration test + demo | `test_integration.py`, demo output | PASS E3 local |
| R13 | NEXY canonical contracts remain untouched | isolated project only | GitHub mutation audit | PENDING PERSISTENCE AUDIT |
| R14 | Persisted bytes match locally verified content | manifest + GitHub readback | publication record | PENDING |
| R15 | Lo4 remains non-canonical until promotion | docs + no NEXY mutation | scope audit | PASS DESIGN; production promotion NOT_AUTHORIZED |
