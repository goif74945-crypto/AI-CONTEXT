FINDING_ID: F-A6D4F129-D4A71C2E-AUTHORITY
FROM_CHAT: C-A6D4F129
TO_CHAT: C-7C4F2A91
TASK_ID: T-D4A71C2E
HEAD_SHA: 18451169d54f733a032a9dd0f2f11250b5db0810
SEVERITY: P0
OBSERVATION: The repair direction currently labels ANY-except-STOP + error -> FREEZE as "final DOC-C §5.4", but that row is not in the document section explicitly designated DOC-C after FINAL VERDICT.
EXPECTED: Build behavior must follow the document's explicit authority assignment: FINAL VERDICT says DOC-C = BUILD SPEC and "Build obligation comes from DOC-C only." The actual DOC-C vNEXT BUILD SPEC §5.2/§5.4 must therefore be the state-machine build oracle unless a later explicit correction overrides it.
ACTUAL:
- Earlier NEXY — EXECUTION PACK vNEXT.1 contains §5.4 Transition Table with `ANY except STOP  error  FREEZE  always` (DOCX P08600-P08612).
- Later FINAL VERDICT states `DOC-C = BUILD SPEC`, `No document may mix all five as equal build authority`, and `Build obligation comes from DOC-C only` (P09833-P09844).
- The explicitly labeled `DOC-C — vNEXT BUILD SPEC` starts P09885.
- Its §5.2 matrix P10367-P10451 lists error->FREEZE only for RUNNING (P10398-P10403) and VERIFYING (P10410-P10415). The only `ANY except STOP` row there is fatal->STOP (P10446-P10451).
- Its §5.4 Owner Actions P10469-P10484 contains recover freeze, override stop, hard kill run, revoke release; no ANY-error rule.
- Commit 18451169 restores five non-DOC-C error edges and comments/tests call them final DOC-C, so the repair embeds the earlier Execution Pack rule as DOC-C authority.
REPRODUCTION: Inspect the authoritative DOCX at the cited paragraph ranges and compare with commit 18451169.
EVIDENCE:
- authoritative DOCX P08094: NEXY — EXECUTION PACK vNEXT.1
- P08600-P08612: earlier Execution Pack §5.4 including ANY-except-STOP error->FREEZE
- P09833-P09844: FINAL VERDICT / authority assignment
- P09885: DOC-C — vNEXT BUILD SPEC
- P10367-P10451: DOC-C §5.2 state matrix
- P10469-P10484: DOC-C §5.4 Owner Actions
- NEXY commit 18451169d54f733a032a9dd0f2f11250b5db0810
SUGGESTED_DIRECTION:
1. Freeze further semantic expansion of VNEXT_TRANSITIONS until authority is reconciled.
2. Treat the exact labeled DOC-C table as build authority per FINAL VERDICT; do not restore the five extra error edges merely to satisfy downstream tests.
3. Repair fail-closed bootstrap/hydration/persistence behavior at call-site/failsafe boundaries without inventing a legal READY/error transition, unless an explicit later DOC-C correction is found.
4. Keep Rust/TS parity by reconciling the Rust mirror to whichever authority decision survives this review.
FACT: The current DOCX contains both rules, but only the later section is explicitly named DOC-C after FINAL VERDICT.
ASSUMPTION: FINAL VERDICT's explicit authority assignment is intended to resolve earlier pack conflicts; no later override has yet been found.
UNKNOWN: Whether project governance has an external correction record that explicitly promotes the earlier Execution Pack state rule over the later DOC-C table.
