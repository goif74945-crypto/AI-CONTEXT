# CIGE Design

## 1. Objective
Produce a deterministic, bounded change-impact analysis that can be replayed from the same graph + change set without hidden environmental inputs.

## 2. Inputs
### Graph
- `schema_version = nexy.cige.v1`
- `nodes[]`
  - `id`: unique non-empty string
  - `kind`: requirement | contract | module | config | artifact | test | evidence
  - `critical`: optional boolean
  - `label`: optional display text
  - `metadata`: optional non-authoritative metadata retained in graph digest
- `edges[]`
  - `from`: consumer/derived/verifier node
  - `to`: dependency/authority/verified target node
  - `type`: depends_on | implements | verifies | derived_from | governed_by | uses

### Change set
Array of changed node IDs. Duplicates are collapsed and canonicalized.

## 3. Edge direction invariant
Every edge points **from the thing that is affected toward the thing it relies on or represents**.

Examples:
- module → contract (`implements`)
- test → module (`verifies`)
- API artifact → module (`depends_on`)
- contract → requirement (`derived_from`)

Therefore change impact is the reverse closure of changed nodes.

## 4. Determinism
The core:
- sorts IDs and edges lexicographically;
- canonicalizes object keys recursively;
- computes SHA-256 over canonical JSON;
- uses deterministic queue ordering;
- does not read clock/RNG/network/filesystem/environment/process state.

The CLI is intentionally outside the core and may read a file. CLI I/O is not part of deterministic authority.

## 5. Output
On PASS:
- graph digest;
- change-set digest;
- canonical changed nodes;
- impacted nodes with distance, edge type, and causal path;
- required test/evidence revalidation frontier;
- critical coverage gaps;
- summary counts.

On invalid/unsafe state:
- `status = FREEZE`
- governed reason code
- deterministic details sufficient to reproduce the failure.

## 6. Failure model
| Condition | Result |
|---|---|
| Invalid schema/ref/type | FREEZE / SCHEMA_VIOLATION |
| Unknown changed ID | FREEZE / UNKNOWN_CHANGED_NODE |
| Hard dependency cycle | FREEZE / DEPENDENCY_CYCLE |
| Graph exceeds configured bounds | FREEZE / GRAPH_LIMIT_EXCEEDED |
| Traversal exceeds configured impact bound | FREEZE / IMPACT_LIMIT_EXCEEDED |
| Invalid limit configuration | FREEZE / INVALID_LIMITS |
| Critical changed node has no reachable test/evidence | FREEZE / EVIDENCE_MISSING |

No result is silently truncated.

## 7. Complexity
For V nodes and E edges:
- validation/indexing: O(V + E)
- hard-cycle scan: O(V + E_hard)
- reverse impact traversal: O(V + E)
- canonical sorting: O(V log V + E log E)

Default bounds are 10,000 nodes / 50,000 edges / 10,000 impacted nodes. These are PROPOSAL_AI defaults, not NEX canonical configuration.

## 8. Security boundary
Untrusted graph input is data only. The engine does not execute node metadata, shell commands, URLs, or code. It has no dynamic import/eval path. Size bounds exist to prevent unbounded traversal. A future host should apply stricter payload-size and schema validation before invocation.

## 9. Compatibility strategy
The engine is intentionally standalone and dependency-free. Integration requires a host adapter that converts authoritative NEXY requirement/contract/module/test/evidence identifiers into this graph schema. The adapter owns authorization, provenance, revision binding, persistence, audit records, and any scheduling of tests.

## 10. Stop conditionsA future integration must FREEZE rather than proceed if:
- authoritative node identity cannot be mapped;
- graph snapshot/revision provenance is missing;
- graph digest differs from the bound execution request;
- required revalidation cannot be scheduled or evidenced;
- integration would bypass LAW/JUDGE/VAULT or other current NEXY authority boundaries.
