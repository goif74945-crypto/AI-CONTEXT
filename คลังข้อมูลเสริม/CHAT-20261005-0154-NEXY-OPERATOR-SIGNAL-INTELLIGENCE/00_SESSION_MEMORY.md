# Temporary Execution Memory

- session_code: `CHAT-20261005-0154-NEXY-OPERATOR-SIGNAL-INTELLIGENCE`
- platform_conversation_id: `UNKNOWN` (not exposed by available tools; not invented)
- repository: `goif74945-crypto/AI-CONTEXT`
- branch: `main`
- authorized_write_root: `คลังข้อมูลเสริม/CHAT-20261005-0154-NEXY-OPERATOR-SIGNAL-INTELLIGENCE/`
- protected_scope: every repository whose name contains `NEXY.AI`, and every existing AI-CONTEXT path outside this new folder
- classification: `AI-PROPOSED / AUXILIARY / NOT CURRENT NEXY SPEC`

## Current state
Reference implementation, local verification, GitHub publication, and exact blob read-back verification are complete for this isolated lab.

## Locked design
Five independent but composable operator-signal systems:
1. Salience Gate
2. Interruption Governor
3. Milestone Compressor
4. Outcome Delta Compiler
5. Acknowledgement Debt Ledger

## Verified local evidence
- Python compileall: PASS
- unittest suite: 55/55 PASS
- branch coverage run: 99% total; production modules 97-100% each
- 10,000 deterministic routing repetitions: one unique canonical result
- static production-boundary scan: no network/subprocess/eval/exec/open calls detected
- CLI subprocess paths exercised by tests

## Publication evidence
- initial publication commit: `ef44eeaa738911e55253d05cd839a7b6da2e8914`
- published file count at that commit: 36
- exact blob read-back: 36/36 matched locally tested/authored bytes
- missing: 0
- mismatched: 0
- extra inside target snapshot: 0
- files outside authorized target in publication commit: 0
- details: `10_PUBLICATION_EVIDENCE.md`

## Important repair history
Two issues were found after the first green run and corrected before publication:
- compressed trailing routine events were mislabeled as `collapsed_before`; contract changed to explicit `trailing_collapsed`;
- empty-root JSON Pointer redaction was accepted but did not redact the full tree; implementation and regression test were fixed.

## Resume rule
For future research or real NEXY adapter work, begin with:
1. `01_TASK_CONTRACT.md`
2. `03_FIVE_CONCEPTS.md`
3. `04_ARCHITECTURE.md`
4. `08_VALIDATION_REPORT.md`
5. `10_PUBLICATION_EVIDENCE.md`

Do not promote this AI proposal to canonical NEXY law without explicit authority and new integration evidence.
