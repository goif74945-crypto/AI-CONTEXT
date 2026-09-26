# NEXY.AI — Legal / ANNEX-T Source Intake

## Purpose

This directory preserves the two uploaded legal/governance source PDFs as complete extracted text with cryptographic provenance, while keeping source claims separate from independently verified legal facts.

## Source set

Source-set ID: NEXY-LEGAL-GOVERNANCE-20260926

1. Guardian Pack (Thailand)
   - Source ID: SRC-NEXY-GUARDIAN-PACK-THAILAND
   - SHA-256: c7809bd04309e30717bb8b37a57dfa569e00da945e3428f1e789015eff78eb6c
   - 5 pages / 98,773 bytes
   - Full text: ./sources/NEXY-GUARDIAN-PACK-THAILAND.fulltext.md

2. ANNEX-T — ABSOLUTE SSOT
   - Source ID: SRC-NEXY-ANNEX-T-ABSOLUTE-SSOT
   - SHA-256: 6ec54767e0b1e899b551ef8b3b3a2c7ce264b1cbc42fbfe3f933d2b390ee8b6e
   - 27 pages / 281,652 bytes
   - Full text reconstruction order:
     1. ./sources/NEXY-ANNEX-T-ABSOLUTE-SSOT.part-01.md
     2. ./sources/NEXY-ANNEX-T-ABSOLUTE-SSOT.part-02.md
     3. ./sources/NEXY-ANNEX-T-ABSOLUTE-SSOT.part-03.md

Machine-readable provenance and scope metadata:
- ./source-manifest.json

## Authority boundary

- ANNEX-T is preserved as a legal/governance canon source for its declared scope.
- The Guardian Pack is preserved as a legal/commercial licensing source/template.
- Their self-declared labels and verdicts are source claims. Ingestion does not independently prove court enforceability, treaty effect, sovereign adoption, legal validity, deployment readiness, or zero-gap completeness.
- These sources do not silently replace DOC-B/DOC-C current build authority. Cross-domain conflicts must be resolved explicitly through the authority graph or current user directive.
- Design/source truth, repository implementation truth, runtime evidence, deployment evidence, and legal validation remain separate evidence classes.

## Completeness

The extracted textual content from both uploaded PDFs is retained in this directory. The original PDF binaries are not duplicated into the repository by this commit; their SHA-256 hashes, sizes and page counts are recorded so later work can identity-match the originals.

## Read order

For legal / ANNEX-T work:
1. source-manifest.json
2. this INDEX
3. relevant full-text source file(s)
4. ../governance/authority-graph.json
5. only then derive requirements, conflicts, contracts or implementation work

Do not convert source-language claims into PASS/evidence without the required verification class.
