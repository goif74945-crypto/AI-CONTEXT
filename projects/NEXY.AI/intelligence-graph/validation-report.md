# NEXY Project Intelligence Graph Validation

## Result
**PASS**

- nodes: **1315**
- edges: **8650**
- dangling edges: **0**
- ontology entities included: **518**
- requirements included: **262**
- contracts included: **22**
- FSM records included: **9**
- invariants included: **28**
- failures included: **22**

The graph preserves:
SOURCE → CLAIM → AUTHORITY → REQUIREMENT → ENTITY → IMPLEMENTATION → TEST → EVIDENCE

and side links:
DEPENDENCY / CONTRACT / FSM / INVARIANT / FAILURE / SUPERSESSION.

No edge upgrades stale evidence into current proof.
