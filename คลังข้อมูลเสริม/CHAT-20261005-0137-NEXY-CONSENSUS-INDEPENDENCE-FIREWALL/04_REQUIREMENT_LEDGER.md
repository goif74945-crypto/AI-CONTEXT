# NCIF Requirement Ledger

**Classification:** EXPERIMENTAL LAB LEDGER

| ID | Requirement | Basis | Implementation / proof | Status |
|---|---|---|---|---|
| NCIF-R01 | Count independent provenance groups, not raw votes | NEXY proof-weighted/cross-verification direction + proposal | DSU connected components; distinct-root and same-root tests | PASS E2 local |
| NCIF-R02 | Propagate evidence ancestry correlation | proposal invariant | iterative topological lineage propagation; parent-lineage test | PASS E2 local |
| NCIF-R03 | Duplicate evidence IDs cannot fabricate lineage | identity integrity | `ensure_unique` + duplicate-ID test | PASS E2 local |
| NCIF-R04 | Same declared root source under different IDs remains correlated | anti-laundering proposal | source-identity digest token; clone attack fixture/test | PASS E2 local |
| NCIF-R05 | Explicit correlation keys propagate through evidence/votes | common-cause declaration | key-token propagation + tests | PASS E2 local |
| NCIF-R06 | Correlation is transitive | independence graph semantics | DSU + bridge-chain tests | PASS E2 local |
| NCIF-R07 | Missing parents fail closed | no guessing / provenance integrity | `MISSING_EVIDENCE_PARENT` | PASS E2 local |
| NCIF-R08 | Cyclic lineage fails closed | invalid provenance DAG | Kahn incomplete-processing detection | PASS E2 local |
| NCIF-R09 | Material votes require evidence | evidence-first | SUPPORT/OPPOSE without evidence → FREEZE | PASS E2 local |
| NCIF-R10 | Independent opposition may block consensus candidate | bounded adversarial review direction | opposition group threshold | PASS E2 local |
| NCIF-R11 | Shared root with opposing stances is conflict | interpretation integrity proposal | cross-stance root overlap check | PASS E2 local |
| NCIF-R12 | Optional single-root removal detects brittle consensus | resilience proposal | remove-root/recluster pass | PASS E2 local |
| NCIF-R13 | Deep valid lineage does not rely on Python recursion | robustness | iterative Kahn algorithm; 1,500 test; 5,000 stress | PASS local bounded stress |
| NCIF-R14 | Result does not directly echo raw source identity/correlation key | privacy minimization | domain-separated digest tokens + leakage test | PASS E2 local |
| NCIF-R15 | Same logical input ordering yields deterministic report/fingerprint | deterministic design | sorted traversal/canonical JSON + permutation tests | PASS E2 local |
| NCIF-R16 | Core has no intentional network/model/random/time dependency | inspectable deterministic core | source inspection + stdlib implementation; no dynamic side-channel audit | PASS E1/source inspection only |
| NCIF-R17 | Result cannot claim final truth/verification | NEXY CORE/JUDGE authority | only `CONSENSUS_CANDIDATE/FREEZE`; `NOT_VERIFIED_FINAL_AUTHORITY` | PASS E2/local inspection |
| NCIF-R18 | Work does not mutate NEXY.AI-named repositories | explicit user directive | all planned persistence targets AI-CONTEXT only | PENDING E0/tool audit until publication |
| NCIF-R19 | Real NEXY integration must be separately proven | verification law | no integration adapter in this lab | NOT_VERIFIED / intentionally out of scope |
| NCIF-R20 | Hidden/undeclared causal dependence must not be falsely claimed detected | truth boundary | documented limitation | PASS documentation; detection itself impossible from absent data |

## Status interpretation

`PASS E2 local` proves only executed behavior of this standalone reference implementation in the recorded local environment. It does not establish NEXY runtime behavior, correctness of caller-supplied provenance, production performance, or deployment readiness.
