# Proposed NEXY Integration Contract

Status: PROPOSAL_AI / NOT CURRENT NEXY REQUIREMENT

## Goal
Allow NEXY to ask CIGE for an impact plan without transferring release authority to CIGE.

## Proposed host flow
1. NEXY authoritative layer resolves an exact project/spec/revision identity.
2. Host builds or loads a graph snapshot bound to that identity.
3. Boundary validator checks graph schema and provenance.
4. Host calls `analyzeImpact(graph, changedIds, limits)`.
5. If CIGE returns FREEZE, host maps it to an authorized NEXY failure path and does not release.
6. If PASS, host treats `required_revalidation` only as a **plan**, not as evidence.
7. NEXY executes the required tests/evidence workflows using its own governed execution path.
8. Only fresh matching evidence may satisfy the release gate.
9. Host persists graph digest + change-set digest + exact evidence references in an auditable record.

## Authority invariant
CIGE MUST NOT:
- mutate NEXY canonical state;
- decide user authority;
- approve release;
- mark tests passed;
- fabricate missing graph edges;
- infer unmapped requirement IDs;
- call external models/providers itself;
- write to Vault or production stores directly.

## Deterministic request proposal
```json
{
  "schema_version": "nexy.cige.request.v1",
  "project_revision": "<authoritative revision id>",
  "graph_digest": "<sha256>",
  "changed_node_ids": ["..."],
  "limits": {
    "maxNodes": 10000,
    "maxEdges": 50000,
    "maxImpactedNodes": 10000
  }
}
```

The placeholder above is documentation syntax only. Production integration must use real authoritative values and reject absent values.

## Proposed output binding
Persist at minimum:
- project/spec revision;
- graph digest;
- change-set digest;
- CIGE code/version digest;
- impacted IDs;
- required revalidation IDs;
- result status/reason code;
- trace/request identity from host;
- fresh evidence IDs after revalidation.

## Failure mapping
CIGE reason codes are proposal-level. A real adapter must map them to current canonical NEXY error taxonomy rather than silently inventing new public API errors.

Suggested internal mapping for design discussion only:
- SCHEMA_VIOLATION → existing schema-validation path
- EVIDENCE_MISSING → existing evidence-missing/release-policy path
- UNKNOWN_CHANGED_NODE / DEPENDENCY_CYCLE / LIMIT failures → FREEZE with an explicit internal incident reason approved by project authority

## Acceptance evidence for future real integration
- E1: adapter type/schema/static validation;
- E2: unit tests for mapping + digest binding;
- E3: integration tests showing impacted tests are scheduled and stale evidence rejected;
- E4: end-to-end flow from authorized change through revalidation and release/freeze;
- E5/E6 only if claiming operational/deployment readiness.
