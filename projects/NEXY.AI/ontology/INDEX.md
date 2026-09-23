# NEXY.AI Atomic Ontology Registry

## Purpose
This directory converts the NEXY source architecture from prose/top-level registry IDs into a graph of explicit engineering objects below the earlier 215-entry registry.

**215 is a top-level tracking baseline, not the atomic object count.**

## Source authority for this pass
Primary source:
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Parsed non-empty paragraph sequence used for source ranges: 10,979 records.

Supporting normalized context:
- `projects/NEXY.AI/deep/`

Supporting context is not allowed to invent entities absent from the source; it is used to preserve authority/evolution/conflict interpretation.

## Files
- `entity-types.json` — ontology type system.
- `entities.jsonl` — one canonical entity per line.
- `relationships.jsonl` — typed graph edges.
- `aliases.json` — canonical-name/legacy-name/era alias map.
- `INDEX.md` — ontology rules and coverage.

## Required entity fields
Every entity carries:
`id, name, aliases, entity_type, parent_id, authority, scope, status, source_range, description, responsibilities, inputs, outputs, dependencies, dependents, contracts, invariants, states, failure_behavior, recovery, security_boundary, persistence, determinism, implementation_refs, test_refs, evidence_refs, supersedes, superseded_by, conflicts`.

Empty arrays mean “not yet established,” not “does not exist.”

## Status semantics
- `CURRENT_CANON` — current source law/canonical concept.
- `CURRENT_BUILD` — part of current DOC-C build obligation.
- `SOURCE_DESIGN` — source-defined design object without current build/runtime proof.
- `FUTURE` — future/extended architecture.
- `HISTORICAL` — retained for provenance; later source evolved away.
- `SUPERSEDED` — an explicit newer entity/claim replaced this semantics.
- `CONFLICT` — source evolution remains unresolved at entity level.
- `NOT_VERIFIED` — implementation/runtime proof absent.
- `UNKNOWN` — status cannot yet be established.

## Scope semantics
- `DOC_B_SYSTEM_LAW`
- `DOC_C_CURRENT_BUILD`
- `DOC_D_PRODUCT_DESIGN`
- `DOC_E_DEPLOYMENT_EVIDENCE`
- `CURRENT_ARCHITECTURE`
- `FUTURE_ARCHITECTURE`
- `EXPERIMENTAL`
- `HISTORICAL`

An entity may have multiple scopes.

## Source ranges
`source_range` uses the local non-empty paragraph sequence from the exact source hash above. These are navigation/provenance anchors, not Word page numbers.

## Graph rule
`relationships.jsonl` is the normalized graph. Inline `dependencies/dependents` in entity records are denormalized navigation helpers and must agree with graph edges after compilation.

## Implementation boundary
Ontology existence does not mean implementation exists. `implementation_refs/test_refs/evidence_refs` remain empty until proven from the actual NEXY implementation/evidence repositories.

## Streaming capture
Ontology construction is performed domain-by-domain:
`READ SOURCE RANGE → EXTRACT → CLASSIFY → DEDUP/ALIAS → WRITE CHECKPOINT → CONTINUE`

Do not regenerate the entire ontology from a single model context or from keyword extraction alone.

## Completion criterion
Atomic ontology is complete for a source revision only when:
1. every major source domain has been processed;
2. aliases/evolution are normalized;
3. graph relationships compile;
4. duplicates are resolved;
5. a coverage summary names remaining UNKNOWN/CONFLICT areas;
6. no exact total is claimed before this normalization pass completes.
