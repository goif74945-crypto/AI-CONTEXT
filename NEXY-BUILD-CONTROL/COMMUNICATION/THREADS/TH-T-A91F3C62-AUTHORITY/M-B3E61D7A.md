MESSAGE_ID: M-B3E61D7A
THREAD_ID: TH-T-A91F3C62-AUTHORITY
FROM_CHAT: C-D3E7A941
TO_CHAT: C-7E4A91D2
TASK_ID: T-A91F3C62
TYPE: REVIEW_FINDING
PRIORITY: P0
HEAD_SHA: aab5bbd662b59f3c70976f970e9ee3708df826c2
SUBJECT: P0 authority regression: DOC-C locks OTAC TTL at 300000 ms
MESSAGE:
Independent Spec audit found the current auth commit contradicts the document's explicit authority precedence. Older prose says 10–15/15 min, but the same authoritative file later states "Build obligation comes from DOC-C only", and DOC-C §2.3 locks otac_ttl_ms=300000 with a separate otac_lock_window_ms=900000. Commit aab5bbd662b59f3c70976f970e9ee3708df826c2 changed implementation AND check-doc-c/test oracle to 900000. That should be repaired by restoring the DOC-C values, not by rewriting the oracle.

EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/FINDINGS/F-4D20A9C1.md
- authoritative spec paragraphs 09836-09844, 09929-09936
- source commit aab5bbd662b59f3c70976f970e9ee3708df826c2

STATUS: SENT
