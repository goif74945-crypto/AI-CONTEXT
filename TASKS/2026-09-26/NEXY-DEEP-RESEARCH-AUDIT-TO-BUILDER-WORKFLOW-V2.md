# NEXY Deep Research Audit→Builder Workflow V2

TASK_ID: NEXY-DEEP-RESEARCH-AUDIT-TO-BUILDER-WORKFLOW-V2
DATE: 2026-09-26
SOURCE: Direct user clarification
STATUS: PROMPT_GUIDANCE

## User-required behavior
Deep Research must not stop at prose summary. It must:
1. Inspect the authoritative design source in detail.
2. Inspect the real implementation repository in detail.
3. Build an evidence-backed comparison table at system/requirement level.
4. Classify each row as:
   - built and matched,
   - built but not matching 100%,
   - missing,
   - out/future scope,
   - unknown/blocker.
5. Only after the comparison matrix is complete, generate dependency-ordered commands for the Builder chat to create/repair/test the missing or mismatched items.
6. Every row and every command must be traceable to source + code/test/evidence proof.
7. No guessing, no summary-only completion, no using stale matrices as current truth.

## Current verified anchors
- AI-CONTEXT main before this record: c171fcd311d7b16cb934df604e93a88a165834cc
- NEXY.ai: 42378126aed29a668f9f294a9100c62a66ff3753
- astra/omega-full-spec-convergence: 1714d8fbb78372e6bd5ddd9bcd8d58599d13dc32
- Source SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

These anchors must be refreshed when the audit starts.

## Completion gate
No BUILDER_COMMAND may be treated as final remediation output until the audit denominator, comparison table, and unresolved/unknown ledger are reconciled.

This record is guidance only; it does not prove that the full audit has been executed.
