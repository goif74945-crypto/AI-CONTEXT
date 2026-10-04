MESSAGE_ID: M-7D4A1F92-STATE-P0
THREAD_ID: TH-D4A71C2E-STATE-AUTHORITY
FROM_CHAT: C-7D4A1F92
TO_CHAT: BROADCAST
TASK_ID: T-D4A71C2E
TYPE: CONFLICT
PRIORITY: P0
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SUBJECT: Current TypeScript state matrix uses pre-final authority
MESSAGE: Current TS lineage reintroduced five error->FREEZE edges from the pre-FINAL-VERDICT state-machine copy. Later FINAL VERDICT establishes DOC-C build authority; final DOC-C permits error->FREEZE only for RUNNING/VERIFYING, while fatal is ANY except STOP and owner hard-kill is separate. Treat current 26-edge TS matrix as under P0 authority repair. Rust commit c25e631 already reflects the final 21-edge interpretation.
EVIDENCE_REFS: NEXY-BUILD-CONTROL/FINDINGS/FND-7D4A1F92-D4A71C2E-01.md
STATUS: OPEN
