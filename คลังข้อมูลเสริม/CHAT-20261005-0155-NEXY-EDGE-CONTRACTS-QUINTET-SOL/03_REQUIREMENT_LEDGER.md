# Requirement Ledger

| ID | Requirement | Implementation | Evidence target |
|---|---|---|---|
| F5-01 | Approval must bind to exact plan identity | `approval_escrow.py` | E2 tamper test |
| F5-02 | Stale epoch/expiry/scope widening must freeze | `approval_escrow.py` | E2 negative tests |
| F5-03 | Evidence planner must choose exact least-cost legal plan | `evidence_closure.py` | E2 optimization test |
| F5-04 | Evidence search limit must never false-PASS | `evidence_closure.py` | E2 limit test |
| F5-05 | Adapter compilation must reject ambiguity/lossy critical drift | `safe_adapter.py` | E2 negative tests |
| F5-06 | Independent quorum must reject shared failure domains | `correlation_quorum.py` | E2 correlation test |
| F5-07 | Policy risk monotonicity violations must produce witnesses | `policy_monotonicity.py` | E2 violation test |
| F5-08 | No third-party runtime dependency | package source | E1 import/compile |
| F5-09 | Deterministic reason ordering/fingerprints | common/core design | E2 repeated assertions |
| F5-10 | NEXY.AI repository must not be mutated | task boundary | repository target evidence |
