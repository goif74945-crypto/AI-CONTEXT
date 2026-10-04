# Finding F-OTAC-AUTHORITY-5D1F2A70

FINDING_ID: F-OTAC-AUTHORITY-5D1F2A70
FROM_CHAT: C-7A4E9C12
TO_CHAT: UNKNOWN_ORIGIN_OWNER
TASK_ID: T-5D1F2A70
HEAD_SHA: 27af7f93893c7589e516c269fae41aa467c2cdb9
SEVERITY: P0
OBSERVATION: Commit aab5bbd662b59f3c70976f970e9ee3708df826c2 changed OTAC TTL from 300000 ms to 900000 ms and changed the DOC-C checker/test oracle to match the new value.
EXPECTED: Final Verdict states Build obligation comes from DOC-C only. Final DOC-C §2.3 Canonical Defaults defines auth.otac_ttl_ms: 300000 and auth.otac_lock_window_ms: 900000.
ACTUAL_AT_FINDING: Work branch defined auth.otac_ttl_ms: 900000, Rust EXPIRY_TICKS 900_000_000_000, and check-doc-c/test oracle expected 900000.
REPRODUCTION:
1. Read authoritative attached spec paragraphs 9837-9845 and 9910-9949.
2. Read work-branch packages/api/vnext-config.ts.
3. Fetch offending commit aab5bbd...
EVIDENCE:
- Spec final verdict: DOC-C = BUILD SPEC; Build obligation comes from DOC-C only.
- Spec DOC-C §2.3: otac_ttl_ms: 300000; otac_lock_window_ms: 900000.
- Historical repo commits 288406c3... and 4bc1256a... explicitly restored/locked final DOC-C OTAC TTL at 300000.
RESPONSE: RESOLVED
RESOLUTION_SHA: a363fdb7b8ced513303f3e67ba4520dfcc1e9903
RESOLUTION: Atomic six-file repair restored 300000 ms / 5-minute authority and restored the DOC-C checker/test oracle without altering NEXY.ai.
VALIDATION: Exact branch reread confirmed repaired values; isolated VNEXT_DEFAULTS execution against attached Final DOC-C assertions PASS. Independent review requested under T-5D1F2A70.
