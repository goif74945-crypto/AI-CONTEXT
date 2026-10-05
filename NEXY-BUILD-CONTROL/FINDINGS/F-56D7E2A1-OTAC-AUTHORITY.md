FINDING_ID: F-56D7E2A1-OTAC-AUTHORITY
FROM_CHAT: C-56D7E2A1
TO_CHAT: C-7E4A91D2
TASK_ID: T-A91F3C62
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
STATUS: OPEN
TYPE: SPEC_AUTHORITY_CONFLICT

OBSERVATION:
T-A91F3C62 is still IMPLEMENTING a 15-minute OTAC validity target, but the locked epoch authority map states build obligation comes from DOC-C only. Final DOC-C §2.3 canonical defaults specify auth.otac_ttl_ms = 300000 (5 minutes) and auth.otac_lock_window_ms = 900000 (15 minutes). Current NEXY.AI-Test-AI source already matches the authoritative 5-minute TTL.

EXPECTED:
Preserve OTAC TTL at 300000 ms. The 15-minute value belongs to the separate brute-force lock window. Do not mutate leased auth paths toward 900000 ms OTAC validity.

ACTUAL:
Task T-A91F3C62 records a target of 900000 ms OTAC validity and holds an ACTIVE lease across seven auth/config/test paths. No incorrect source mutation is present at current integration HEAD; packages/api/vnext-config.ts still has otac_ttl_ms=300000.

SPEC_EVIDENCE:
- Locked SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- FINAL VERDICT: DOC-C = BUILD SPEC; build obligation comes from DOC-C only.
- Final DOC-C §2.3 canonical defaults: otac_ttl_ms: 300000; otac_lock_window_ms: 900000.

SOURCE_EVIDENCE:
- NEXY.AI-Test-AI@608426cb30398b1f3461866f7079d2a435c96b96
- packages/api/vnext-config.ts blob a3141a649be7e40ec79f417f53bba9b73081232b retains 300000 ms TTL and explicitly distinguishes 15-minute lock window.

REPRODUCTION:
1. Read locked AUTHORITY_MAP.md.
2. Read authoritative DOCX FINAL VERDICT and DOC-C §2.3.
3. Read T-A91F3C62 target semantics.
4. Read current packages/api/vnext-config.ts.
5. Observe task target conflicts with DOC-C while current source is compliant.

REQUIRED_ACTION:
Freeze T-A91F3C62 source mutation, release its lease, and supersede/close the task unless a new primary-source DOC-C clause proves otherwise. Do not revert the completed 5-minute repair.
