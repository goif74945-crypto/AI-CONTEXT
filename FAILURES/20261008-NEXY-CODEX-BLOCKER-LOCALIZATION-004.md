# FAILURE — NEXY Cross-Chat Source and Runner Gaps

FAILURE_ID: 20261008-NEXY-CODEX-BLOCKER-LOCALIZATION-004
TASK_ID: 20261008-NEXY-CODEX-NEXT-COMMAND-004
MODE: CROSS / AUDIT
STATUS: RECORDED

CONTEXT:
Codex reported release verification PARTIAL at product HEAD 8b406a63f10aa1424225a80453393af2e4cb78b5. Browser 9 pass/2 fail, experimental 781 pass/10 fail, four spec access blocks, five infrastructure blocks.

FAILED_APPROACH:
Treating all missing DOCX, TSA runtime, sandbox root mismatch, and CI zero-step failures as a single reason to stop further independent work.

CAUSE:
Different subsystem dependencies and evidence authority levels were not yet resolved at the product runtime. Browser failure may include missing trusted time bootstrap; experimental failure may be a bwrap host path issue; GitHub CI cause remains unknown.

RECOVERY:
- Reuse only SHA-matched source extracts with exact paragraph locators.
- Trace full production TSA call graph and prove whether DOC-C requires the hard dependency; do not fabricate clock or signatures.
- Reproduce bwrap host-executable mismatch and preserve isolation.
- Investigate CI failures without assuming historic billing diagnosis.
- Continue bounded substantive audits of the remaining NOT_VERIFIED rows.
- Preserve local blocker semantics.

BOUNDARIES:
No test weakening, no fake release signoffs, no synthetic production time, no untrusted arbitrary host mount, no mass promotion of matrix rows, no branch topology mutations.

PREVENTION:
Maintain separate capability/readiness classifications; exact HEAD and source-bound evidence; source hierarchy DOC-C vs broader architecture; final DOC-E gate.

REGRESSION:
Codex next-command 004 requires targeted browser and experimental rerun with actual evidence and final-head revalidation after edits.

FINAL_STATUS: FAILURE_CAPTURED_WITH_RECOVERY_PLAN
