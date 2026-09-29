# NEXY.AI Requirement Registry

## Current completeness warning
**The existing `requirements.jsonl` is a prior partial registry and is not the exhaustive current denominator.**

Current exhaustive source enumeration is recorded in:
`projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`

Current normalized matrix: **837 rows**.

The historical 215-entry registry is `DEPRECATED_UNRELIABLE_DO_NOT_USE` and must not be used to fill gaps or define the denominator.

The existing 262 requirement records remain useful for historical traceability and their own internal links, but **262 must not be presented as the complete NEXY source requirement count**.

## Purpose
Convert source prose into discrete, traceable, testable requirements.

Canonical trace spine:

`SOURCE → REQUIREMENT → ONTOLOGY ENTITY → IMPLEMENTATION → TEST → EVIDENCE → VERDICT`

This registry only establishes the first three links for now.

## Files
- `requirements.jsonl` — canonical requirement records.
- `requirement.schema.json` — machine validation schema.
- `coverage.json` — counts by authority/scope/priority/status.
- `validation-report.md` — structural validation.
- `checkpoints/` — streaming source-domain extraction checkpoints.

## Status rule
Until implementation/test/evidence mapping occurs, a requirement is not PASS merely because source prose exists.

Default implementation status:
`UNKNOWN` or `NOT_VERIFIED`.

## Priority semantics
- `MUST` — source expresses mandatory/locked/required behavior.
- `SHOULD` — explicit target/direction with allowed implementation variance.
- `MAY` — optional/allowed behavior or example.

Priority is source semantics, not business priority.

## Authority semantics
Requirements preserve source authority such as:
- DOC-B System Law
- DOC-C current build spec
- DOC-D product design
- DOC-E deployment evidence
- Constitutional locked source
- L600 source
- Final architecture synthesis

They are not flattened into one authority level.

## Source revision
Primary source:
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- paragraph-index basis: 10,979 non-empty extracted records.

## Streaming rule
Requirements are extracted domain-by-domain and checkpointed immediately.
A later compiler deduplicates/validates IDs and ontology references.

## Implementation boundary
`implementation_refs`, `test_refs`, and `evidence_refs` remain empty until their dedicated mapping/audit steps.
