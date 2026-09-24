# Semantic Diff + Change Impact Validation

## Result
**PASS — first-class structural/query integration**

Observed AI-CONTEXT input HEAD: `7748e64c1a4d526f6fbde67277c1292a3e07b865`

- ontology entities: **518**
- canonical change-impact records: **518**
- reconciled per-entity impact records: **518**
- duplicate/missing entity IDs: **0**
- dangling prerequisite/dependent references: **0**
- reconciled records: `EVENT-EXEC-CANCEL`, `EVENT-EXEC-TIMEOUT`
- change types CODE/CONFIG/SCHEMA/STATE/PERMISSION/CONTRACT/REQUIREMENT_SPEC: PASS
- EXACT/CANDIDATE/UNKNOWN buckets: PASS
- golden code/config examples: PASS
- filename-only mapping remains non-EXACT: PASS
- semantic-diff + intelligence-graph + invariants + traceability integration contract: PASS

Boundary: structural/derived validation only; no runtime breakage or runtime PASS is inferred.
