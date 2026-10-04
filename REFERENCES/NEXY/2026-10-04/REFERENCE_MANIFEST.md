# NEXY External Reference Manifest — 2026-10-04

Purpose: preserve the non-repository reference material that was actually used during NEXY.AI specification/code audits and percentage discussions.

## Scope

Included:
- user/library design source used as specification authority;
- integrity checkpoint for that source;
- system/feature matrices used for requirement and percentage work;
- BA33C8F row ledger and full audit;
- earlier AB471D1 audit retained to show historical revision drift.

Excluded:
- every file whose source of truth is already inside `goif74945-crypto/NEXY.AI-`;
- ChatGPT temporary memory, hidden context, scratchpad, or transient reasoning;
- unrelated library files that were not used as audit/reference material.

## Reference files

### 04-NEXY-IGNIS-source.txt
Parsed-text snapshot of the authoritative `04-NEXY-IGNIS-.docx`.
Verified original source SHA-256:
`b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.

Contains NEXY/IGNIS design/canon material including DOC-A/B/C/D/E, current build law, product design, deployment evidence definitions, Sovereign/Universe/Game/NCF/L1o/Lo3/Lo2/Robotics and final architecture material.

Important: the original DOCX remains authoritative. This repository file is a parsed-text retrieval snapshot, not a byte-for-byte DOCX replacement.

### NEXY_IGNIS_ingestion_checkpoint.md
Provenance and ingestion-integrity evidence for the design source. It records:
- source SHA-256 and byte size;
- 293 parser pages;
- 12,054 parser lines;
- 10,979 indexed textual records;
- 15,044 OOXML text nodes;
- ordered reconstruction coverage 15,044/15,044;
- exact ordered-text reconstruction PASS.

### NEXY_IGNIS_FULL_SYSTEM_FEATURE_BUILD_MATRIX.txt
Parsed-text snapshot of the XLSX build matrix used to enumerate requirements and systems.
Contains normalized requirement rows, parent systems, features, descriptions, authority, build scope, source locations, dependencies, validation-evidence fields and implementation-status fields.

Important: the original XLSX remains the source workbook. This is a text snapshot for repository retrieval.

### NEXY_FULL_PROJECT_SYSTEM_FEATURE_PERCENT_MATRIX.txt
Parsed-text snapshot of the generated project matrix used in later percentage/comparison work.
Contains Major Summary, System Summary, Master Matrix and Audit Basis information.
It includes historical BA33C8F percentages and later DOC-E treatment. Historical values must not be silently promoted to a newer implementation HEAD.

### NEXY_SPEC_CODE_AUDIT_ROWS_BA33C8F.csv
Machine-readable BA33C8F audit row ledger.
Fields include domain, system, feature, status, evidence, note and source range.

### NEXY_FULL_SPEC_CODE_AUDIT_FINAL_BA33C8F.md
Full source-to-code audit revalidated at implementation HEAD:
`ba33c8fdcd0ea56729835bf06b43500ec5b21f4e`.

Contains the audit lock, scoring method, system matrix, DOC-C/DOC-D/DOC-E interpretation and full-file extension findings. It is historical evidence for that exact revision, not proof of any later HEAD.

### NEXY_FULL_SPEC_CODE_AUDIT_FINAL_AB471D1.md
Earlier historical source-to-code audit at:
`ab471d1e2705d6010afdcdbb0a7baf08132de47d`.

Retained to make revision drift and audit evolution inspectable.

## Truth hierarchy

1. Design/spec truth = authoritative NEXY-IGNIS source at the locked source SHA.
2. Implementation truth = exact code in `goif74945-crypto/NEXY.AI-` at the named commit/ref.
3. Test truth = executed test/evidence bound to that exact implementation revision.
4. Historical audit files describe only the revisions they explicitly name.
5. If source, code, tests and old audits disagree, do not average them. Mark the conflict and re-audit the exact current HEAD.

## Binary-source note

The connected GitHub write interface stores UTF-8 repository content. DOCX/XLSX references were therefore transferred as parsed-text snapshots with explicit provenance. They are not falsely labeled as original binary files.
