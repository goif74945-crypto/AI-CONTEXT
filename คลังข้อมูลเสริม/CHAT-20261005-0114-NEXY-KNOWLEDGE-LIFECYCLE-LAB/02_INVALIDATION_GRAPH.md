# Dependency-Aware Invalidation Graph
> Classification: AI-PROPOSED CONCEPT.

## Objective
Prevent stale facts from surviving because they were copied into summaries, plans, prompts, caches, indexes, or generated artifacts.

## Model
Represent knowledge as a directed graph:
EVIDENCE -> CLAIM -> DECISION -> ARTIFACT -> ACTION.

An edge means the child materially depends on the parent. Each edge has criticality: HARD, SOFT, INFORMATIONAL.

## Propagation
When a node becomes INVALIDATED:
1. Traverse HARD descendants immediately.
2. Mark dependent claims REVALIDATION_REQUIRED.
3. Mark decisions IMPACT_REVIEW_REQUIRED.
4. Mark executable artifacts BLOCKED if the invalidated dependency can alter behavior.
5. Do not automatically delete historical artifacts. Preserve them with invalidation metadata.

SOFT dependencies lower confidence but do not automatically block.
INFORMATIONAL dependencies produce trace notes only.

## Blast-radius query
Given node X, return:
- direct dependents
- transitive HARD dependents
- user-visible outputs affected
- executable actions affected
- required revalidation order
- estimated verification cost

## Anti-patterns
- timestamp-only freshness
- silent overwrite
- treating embeddings as provenance
- assuming a newer source is automatically more authoritative
- deleting contradictory evidence instead of recording conflict
