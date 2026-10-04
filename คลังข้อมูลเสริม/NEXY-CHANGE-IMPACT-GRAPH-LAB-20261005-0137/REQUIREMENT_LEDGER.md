# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| CIGE-R01 | Core deterministic for same semantic graph + change set | task + PROPOSAL_AI design | `normalizeGraph`, canonical sorting, stable stringify | unit tests deterministic digest/output | PASS |
| CIGE-R02 | Core has no clock/RNG/network/filesystem/environment/process input | task + NEXY-aligned constraint | `src/impact_graph.mjs` imports only `node:crypto` | static source inspection + syntax check | PASS |
| CIGE-R03 | Unknown changed node must not be guessed/dropped | task | `UNKNOWN_CHANGED_NODE` FREEZE | unit test | PASS |
| CIGE-R04 | Invalid graph/reference/type must FREEZE | task | `validateGraph` | unit test | PASS |
| CIGE-R05 | Hard dependency cycle must FREEZE | design invariant | DFS cycle check | unit test | PASS |
| CIGE-R06 | Impact must propagate from dependency to all known consumers | design | reverse adjacency + BFS | unit tests | PASS |
| CIGE-R07 | Output must explain causal paths | design | `buildCausePath` | unit test exact path | PASS |
| CIGE-R08 | Impacted tests/evidence become revalidation frontier | objective | `required_revalidation` | unit tests + demo | PASS |
| CIGE-R09 | Critical changed node without reachable verification coverage FREEZEs | objective | critical coverage scan | unit test | PASS |
| CIGE-R10 | Bounded graph/traversal; no silent truncation | security/reliability | graph + impact limits | unit tests | PASS |
| CIGE-R11 | Standalone code must not modify NEXY.AI repo | explicit user constraint | all writes scoped to sandbox then AI-CONTEXT | repo target audit | PASS |
| CIGE-R12 | Real NEXY integration claims require evidence and are not implied | AI-CONTEXT verification law | docs label NOT_VERIFIED | artifact audit | PASS |
