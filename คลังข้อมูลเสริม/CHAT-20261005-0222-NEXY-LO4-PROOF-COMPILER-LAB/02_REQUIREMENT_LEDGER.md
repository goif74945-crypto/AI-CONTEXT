# Requirement & Evidence Ledger

Status: execution-time ledger for this Lo4 proposal workspace.

| ID | Requirement | Required evidence | Current target |
|---|---|---|---|
| R-APS-01 | Reject unreceipted upward authority escalation | E2 | `authority.py` tests |
| R-APS-02 | Detect authority lineage cycle/missing identity | E2 | `authority.py` tests |
| R-APS-03 | Seal deterministically | E2 | digest order test |
| R-UCL-01 | Propagate uncertainty only along dependencies | E2 | containment test |
| R-UCL-02 | Reject cycles/missing dependencies | E2 | negative tests |
| R-MPP-01 | Never substitute lower evidence class | E2 | evidence-class test |
| R-MPP-02 | Choose exact minimum cost under bound | E2 | optimization test |
| R-MPP-03 | Fail closed when impossible/out of exact bound | E2 | negative tests |
| R-RBWE-01 | Generate deterministic positive/negative/missing witnesses | E2 | witness execution tests |
| R-RBWE-02 | Detect selected direct contradictions | E2 | contradiction tests |
| R-RBWE-03 | Reject unsupported operator instead of guessing | E2 | negative test |
| R-PCOC-01 | Release only fully supported claims | E2 | compiler happy path |
| R-PCOC-02 | Freeze invalid authority/uncertainty/evidence | E2 | negative tests |
| R-PCOC-03 | Produce deterministic digest independent of input order | E2 | digest test |
| R-INT-01 | Compose all five modules in one deterministic reference flow | E3 (isolated package integration) | integration test |
| R-SCOPE-01 | No NEXY.AI repository mutation | E0/Evidence audit | mission records |
| R-STATUS-01 | All artifacts remain proposal-only | E0/E1 | headers/readback |

No row in this ledger claims production NEXY integration.
