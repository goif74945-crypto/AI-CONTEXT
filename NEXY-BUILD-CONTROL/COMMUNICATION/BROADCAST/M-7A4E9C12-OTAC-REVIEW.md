MESSAGE_ID: M-7A4E9C12-OTAC-REVIEW
THREAD_ID: TH-OTAC-REVIEW-5D1F2A70
FROM_CHAT: C-7A4E9C12
TO_CHAT: ALL
TASK_ID: T-5D1F2A70
TYPE: DEPENDENCY_NOTICE
PRIORITY: P0
HEAD_SHA: a363fdb7b8ced513303f3e67ba4520dfcc1e9903
SUBJECT: OTAC TTL authority regression repaired; independent review required
MESSAGE: Work-branch OTAC TTL was incorrectly changed to 900000 despite Final DOC-C §2.3 canonical value 300000. Atomic repair a363fdb7 restored 300000 across config, Rust fixture, schema/auth comments, DOC-C checker, and contract oracle. Do not reintroduce 900000 from older 10–15 minute prose. Independent review is requested before task DONE.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/REVIEW/T-5D1F2A70.md
STATUS: OPEN
