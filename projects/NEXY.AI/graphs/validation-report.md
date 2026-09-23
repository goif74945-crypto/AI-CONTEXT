# Dependency Graph Validation

## Result
**PASS — structural dependency graph**

- nodes: **516**
- edges: **863**
- full `REQUIRES` graph acyclic: **true**
- current DOC-C relevant nodes (including transitive prerequisites): **116**
- current DOC-C `REQUIRES` graph acyclic: **true**
- reserved TESTS edges: 0 (intentional; populated later)
- reserved PROVES edges: 0 (intentional; populated later)

## Build-order authority
Current DOC-C explicitly locks the high-level order:

`Contract Lock → Core → Law → Swarm → Judge → Vault → Auth → Observability → API → UI`

The graph stores this separately as `canonical_phase_order` rather than pretending every source dependency edge alone can reconstruct product build sequencing.

## Direction rule
A `REQUIRES` record is:

`dependent → prerequisite`

For task/build DAG generation, reverse it:

`prerequisite → dependent`.

## Warning
Semantic edges such as GOVERNS/OVERRIDES/OBSERVES are not build dependencies and must not be topologically sorted as if they were REQUIRES.
