# Requirement / Evidence Ledger

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| FAB-R001 | Exactly five distinct engines are implemented. | package modules + demo | PASS |
| FAB-R002 | Runtime verdict paths use Python standard library only. | import/static inspection | PASS |
| FAB-R003 | Invalid material input fails closed. | negative tests | PASS |
| FAB-R004 | Set-like input permutation does not alter semantic result/fingerprint where order is non-authoritative. | permutation tests | PASS |
| GCG-R001 | Every work item must contribute to at least one declared criterion. | `test_orphan_freezes` | PASS |
| GCG-R002 | Every criterion must be covered. | outcome engine + tests | PASS |
| GCG-R003 | Forbidden scope, bad dependencies and cycles freeze. | negative tests | PASS |
| VCC-R001 | Only AVAILABLE capabilities are eligible. | unavailable test | PASS |
| VCC-R002 | Data/permission/risk/cost/step constraints bound composition. | policy/budget tests | PASS |
| VCC-R003 | Selection is deterministic under manifest permutation. | permutation test | PASS |
| ACFG-R001 | Required files/media/metadata/size/classification are enforced. | artifact tests | PASS |
| ACFG-R002 | Declared SHA-256 must match actual content when required. | hash mismatch test | PASS |
| SCTG-R001 | Pinning, digest, source and signature policy are enforced. | supply-chain tests | PASS |
| SCTG-R002 | Excess permissions/network domains freeze. | negative tests | PASS |
| MPC-R001 | Path is derived from explicit prerequisites and declared knowledge only. | mastery tests | PASS |
| MPC-R002 | Cycles, unknown goals/references and step overflow freeze. | negative tests | PASS |
| FAB-R005 | Static Python compilation succeeds. | compileall | PASS |
| FAB-R006 | Full test suite succeeds after final code changes. | `31 passed` | PASS |
| FAB-R007 | Package-level five-engine demo succeeds. | demo output | PASS |
| FAB-R008 | Repeated demo output is byte-identical. | two-run `cmp` + SHA-256 | PASS |
| FAB-R009 | Persisted AI-CONTEXT bytes are fetch/read-back verified. | repository verification | PENDING UNTIL PUBLISH |
| FAB-R010 | NEXY.AI runtime integration works. | none | NOT_VERIFIED |
| FAB-R011 | Users prefer these systems / measurable product value improves. | none | NOT_VERIFIED |
