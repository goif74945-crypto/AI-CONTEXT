# NEXY.AI Dependency Graph

Canonical files:
- `dependency-graph.json` — full typed graph + current DOC-C build graph.
- `dependency-graph.mmd` — compact Mermaid view of locked build phases and high-level current dependencies.
- `validation-report.md` — DAG/reference semantics.

Source:
- Atomic Ontology v1.
- Requirement Registry v1.
- DOC-C locked build order.

## Key property
`REQUIRES` is acyclic and therefore safe to use as a base for automatic Task DAG generation.

Authority/control/observability relationships remain separate semantic edge types and do not contaminate the build DAG.

## Reserved future edge types
`TESTS` and `PROVES` are already part of graph vocabulary but remain empty until the Acceptance/Test Matrix and Evidence Registry exist. No fake edges are generated.
