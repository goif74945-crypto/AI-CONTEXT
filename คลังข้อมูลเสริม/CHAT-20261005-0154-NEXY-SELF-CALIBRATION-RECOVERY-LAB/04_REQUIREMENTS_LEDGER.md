# Requirements Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R01 | Five materially distinct concepts | `concepts/*/DESIGN.md` + source modules | novelty matrix + 38-test suite | PASS_LOCAL |
| R02 | Observed behavior must not become authority | Contract Archaeologist hard-coded authority label | miner tests + demo | PASS_LOCAL |
| R03 | Safe interruption/resume must fail closed on unsafe in-flight work or state drift | PauseSafe Kernel | kernel tests + state matrix | PASS_LOCAL |
| R04 | Correlated evidence must not inflate independent count | Evidence Genealogy Engine | auditor tests + transitive genealogy adversarial test | PASS_LOCAL |
| R05 | Concrete failures should shrink to explicit 1-minimal witness | Failure Atomizer | atomizer tests + all 28 trigger-pair matrix | PASS_LOCAL |
| R06 | Confidence should be evaluated against verified outcomes, not self-belief | Calibration Observatory | calibrator tests + balanced population adversarial test | PASS_LOCAL |
| R07 | Deterministic canonical identity | `core/canonical.py` + content-derived report fingerprints | repeated/permutation tests | PASS_LOCAL |
| R08 | No hidden I/O/network/model/subprocess in reference core | source inspection + standard library only | source files + compileall | PASS_STATIC_LOCAL |
| R09 | Cross-system composition exists | `integration/test_portfolio.py`, `demo.py` | E3-local execution | PASS_LOCAL |
| R10 | Future NEXY compatibility is adapter-based and non-authoritative | design contracts | architecture review | DESIGN_ONLY |
| R11 | No repository whose name contains NEXY.AI is mutated | mutation scope restricted to AI-CONTEXT mission folder | GitHub commit/diff audit required | PENDING_GITHUB_AUDIT |
| R12 | Persisted critical source matches tested local content | manifest/read-back hashes | GitHub read-back required | PENDING_GITHUB_AUDIT |
