# Change Impact Validation Report

## Result
**PASS — derived graph/data integrity**

- entity impact records: **516**
- ontology entities: **516**
- dependency graph nodes: **516**
- invariant records: **50**
- failure records: **24**
- traceability records: **262**
- impact records missing entity target: **0**

## Derivation checks
- one impact record per ontology entity: PASS
- direct impact derived from typed graph, not prose guessing: PASS
- transitive REQUIRES closure computed: PASS
- known failures linked by canonical entity name/aliases when resolvable: PASS
- invariants linked by canonical entity name/aliases when resolvable: PASS
- mapped tests/evidence remain navigation/proof references from traceability; no PASS promotion: PASS

## Limitation
Name/alias matching can leave valid invariant/failure links unmapped when source records use a broad subsystem label with no exact ontology alias. Future Intelligence Graph compilation should replace residual name matching with explicit IDs.
