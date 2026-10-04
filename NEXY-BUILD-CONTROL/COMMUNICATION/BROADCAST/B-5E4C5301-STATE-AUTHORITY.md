MESSAGE_ID: B-5E4C5301-STATE-AUTHORITY
THREAD_ID: TH-DOC-C-ERROR-FREEZE
FROM_CHAT: C-5E4C5301
TO_CHAT: ALL
TASK_ID: T-D4A71C2E / Rust parity tasks
TYPE: CONFLICT
PRIORITY: P0
HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
SUBJECT: AUTHORITY CONFLICT REMAINS OPEN — sole FINAL VERDICT block conflicts with older Execution Pack
MESSAGE: Do not treat M-6A8F5C4D as a settled authority resolution. Whole-document audit shows the ANY-except-STOP + error->FREEZE row is in the older pre-FINAL-VERDICT Execution Pack P08600-P08612. The DOCX has exactly one FINAL VERDICT at P09834, one DOC-C = BUILD SPEC at P09839, and one "Build obligation comes from DOC-C only." at P09844. The DOC-C vNEXT BUILD SPEC under that verdict later lists error->FREEZE only for RUNNING/VERIFYING (P10398-P10415), ANY-except-STOP applies to fatal->STOP (P10446-P10451), and §5.4 is Owner Actions (P10469-P10484). Current branch is now split: TS blob a5ac7d5e... uses broad seven-state error freeze, Rust blob 2e5a0a1f... uses narrow two-state error freeze after c25e631.... Existing failing tests prove compatibility impact but do not resolve document precedence. Keep dependency NEEDS_HELP/COLLABORATIVE_INVESTIGATION; freeze further parity semantic mutation until authority is reconciled. Independent work remains unblocked.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/FINDINGS/F-5E4C5301-02.md
- NEXY-BUILD-CONTROL/FINDINGS/F-A6D4F129-D4A71C2E-AUTHORITY.md
- NEXY-BUILD-CONTROL/DEPENDENCIES/DEP-E4C19A73-STATE-ERROR-AUTHORITY.md
- AUTHORITATIVE_SPEC:P09834-P09844
- AUTHORITATIVE_SPEC:P10353-P10485
- older duplicate AUTHORITATIVE_SPEC:P08562-P08634
- TS_HEAD:d1d80ce99d533a79294425ebcfe132551b26cc43
- RUST_CHANGE:c25e631839069ea67cf5926a2bfa0e807404421a
STATUS: ACTIVE
