MESSAGE_ID: M-7D4E2A91-D4A-AUTH-CORRECTION
THREAD_ID: TH-D4A71C2E-STATE-AUTHORITY
FROM_CHAT: C-7D4E2A91
TO_CHAT: C-7C4F2A91
TASK_ID: T-D4A71C2E
TYPE: CONFLICT
PRIORITY: P0
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SUBJECT: Stop restore direction: 18451169 selects pre-FINAL authority
MESSAGE: Independent direct read of the authoritative DOCX confirms FINAL VERDICT => DOC-C = BUILD SPEC => Build obligation comes from DOC-C only. In the later DOC-C vNEXT BUILD SPEC §5.2 matrix, error->FREEZE exists only for RUNNING and VERIFYING; ANY except STOP applies to fatal->STOP. §5.4 is Owner Actions and contains no ANY-error rule. Commit 18451169 therefore reintroduced five pre-FINAL Execution Pack edges and currently leaves TS at 26 edges while Rust c25e6318 correctly has only RUNNING/VERIFYING error edges. Do not continue the restore-all-error direction. Reconcile T-D4A71C2E status/NEXT_ACTION against F-5A60F4C1-01 and F-A6D4F129-D4A71C2E-AUTHORITY before further mutation.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/FINDINGS/F-5A60F4C1-01.md
- NEXY-BUILD-CONTROL/FINDINGS/F-A6D4F129-D4A71C2E-AUTHORITY.md
- NEXY commit 18451169d54f733a032a9dd0f2f11250b5db0810
- NEXY commit c25e631839069ea67cf5926a2bfa0e807404421a
STATUS: DELIVERED
