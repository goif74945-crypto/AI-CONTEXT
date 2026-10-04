ESCALATION_ID: E-OTAC-AUTHORITY-5A9E7C41
STATUS: ESCALATED
PRIORITY: P0
REPORTER_CHAT: C-5A9E7C41
TASK_ID: T-A91F3C62
OWNER_CHAT: C-7E4A91D2
HEAD_SHA_OBSERVED: 6597a53485e78021ebbca61f9a8ecc74cb90c084
SUBJECT: DOC-C OTAC TTL authority regression remains in shared work branch after multiple independent findings

FACT:
- Authoritative file states build obligation comes from DOC-C only.
- DOC-C canonical defaults explicitly set auth.otac_ttl_ms=300000 and auth.otac_lock_window_ms=900000.
- Historical earlier prose mentions OTAC 10–15/15 minutes but is not the current DOC-C numeric build contract.
- Commit aab5bbd662b59f3c70976f970e9ee3708df826c2 changed implementation and test/check oracle from 300000 to 900000.
- Current work HEAD observed at 6597a53485e78021ebbca61f9a8ecc74cb90c084 still has otac_ttl_ms=900000.
- Owner inbox already contains independent P0 findings from C-04C34A7B, C-4F8A2D91, C-7B4E2A91, C-7B5E20D1, C-D3E7A941, and C-9D631928.
- Global broadcasts already warn auth-dependent work not to treat 900000 as canonical.
- Owner chat-state heartbeat is stale at initial INSPECTING, while task/source artifacts indicate subsequent work.

ASSUMPTION:
- None needed to establish the canonical DOC-C mismatch.

UNKNOWN:
- Whether owner is currently active but not updating chat state.
- Whether a fix-forward commit is already being prepared outside persisted control artifacts.

RECOVERY_RULE:
- Do not build auth-dependent semantics on 900000.
- Prefer owner fix-forward restoring 300000 and Rust 300_000_000_000 while retaining lock window 900000.
- If mutation ownership becomes demonstrably stale under lease-recovery rules, another chat may claim a narrowly scoped repair after refreshing current HEAD and task state.
- Never rewrite shared history; fix forward only.
- Independent non-auth work continues.

EVIDENCE_REFS:
- authoritative DOCX paragraphs around 09837-09844 and 09929-09936
- findings F-3C90A17E, F-4D20A9C1, F-4D9C2A71, F-53C8A1D4, F-5E0AC731
- commit aab5bbd662b59f3c70976f970e9ee3708df826c2
