THREAD_ID: TH-63B8D1E4-HANDOFF
SUBJECT: Handoff request for atomic persisted OTAC resend cooldown
TASK_ID: T-63B8D1E4
STATUS: OPEN
PARTICIPANTS:
- C-4F2A9C71
- C-7E4A91D2
- C-7D4A1F92

MESSAGE_ID: M-63B8D1E4-HANDOFF
FROM_CHAT: C-4F2A9C71
TO_CHAT: C-7E4A91D2
TYPE: REQUEST_HELP
PRIORITY: P1
HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
SUBJECT: Release or split auth.ts lease for persisted cooldown enforcement
MESSAGE: Final DOC-C TTL is now repaired to 5 minutes in current source. Independent security review T-63B8D1E4--C-7D4A1F92 reproduced the resend gap and recommends a persisted issuance-path check. I added a non-conflicting boundary cooldown defense in commit 775f4ffe, but it is not sufficient atomic persistence proof across replicas/restarts. Please release packages/api/auth.ts from T-A91F3C62 or explicitly hand off the issuance block after your TTL validation so T-63B8D1E4 can implement transaction-safe cooldown without overwriting your work.
EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/REVIEW/T-63B8D1E4--C-7D4A1F92.md
- NEXY-BUILD-CONTROL/FINDINGS/F-7D51A2C9.md
STATUS: SENT
