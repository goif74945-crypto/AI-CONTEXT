# Governance Validation Report

## Result
**PASS — structural governance validation**

- authority nodes: **15**
- authority edges: **20**
- scope classes: **11**
- claim nodes: **16**
- claim-level supersession edges: **8**
- requirement-level supersession edges: **10**
- conflict/distinction records: **8**
- unresolved records: **1**

Checks:
- authority edge endpoints exist: PASS
- supersession claim endpoints exist: PASS
- requirement supersession endpoints exist: PASS
- conflict affected ontology entities exist: PASS
- future/current scope distinction is explicit: PASS

## Unresolved
- `CONFLICT-RCL-LATENCY-001`

## Interpretation
Resolved distinctions remain in `conflicts.jsonl` deliberately so future AI does not rediscover and misclassify them.

Only records with an unresolved status should block a decision that depends on the unresolved semantic.

This validation does not prove implementation behavior.
