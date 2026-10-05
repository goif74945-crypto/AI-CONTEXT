# Independent HEAD Reverify — T-5D1F2A70

CHAT_ID: C-3B5E71A2
ROLE: Independent Reviewer / Spec Auditor
TASK_ID: T-5D1F2A70
REVIEW_TYPE: FRESH_HEAD_SCOPED_REVERIFY
SPEC_ID: NEXY-IGNIS-b35ee1bf82125792
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
INTEGRATION_BRANCH: NEXY.AI-Test-AI
INTEGRATION_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16
REPAIR_SHA: a363fdb7b8ced513303f3e67ba4520dfcc1e9903
REVIEWED_AT_LOCAL: 2026-10-05T17:40:00+07:00

## Authoritative obligation

Final Verdict establishes DOC-C as BUILD SPEC and says build obligation comes from DOC-C only.
Final DOC-C §2.3 canonical auth defaults require:
- otac_length = 10
- otac_ttl_ms = 300000
- otac_max_attempts = 5
- otac_resend_cooldown_ms = 60000
- otac_lock_window_ms = 900000
- session_ttl_ms = 21600000
- concurrent_sessions_per_user = 5

## Exact-head source reverify

At integration SHA 608426cb30398b1f3461866f7079d2a435c96b96:
- packages/api/vnext-config.ts: otac_ttl_ms = 300_000 and otac_lock_window_ms = 900_000.
- packages/api/auth.ts: OTAC expiry derives from VNEXT_DEFAULTS.auth.otac_ttl_ms; lock window remains separately derived from otac_lock_window_ms.
- core-kernel/src/auth/gatekeeper.rs: EXPIRY_TICKS = 300_000_000_000 with the repository's documented 5-minute @ 1 GHz fixture mapping.
- prisma/schema.prisma: OTAC pending expiry comments state final DOC-C +5 minutes; brute-force lock remains 15 minutes.
- scripts/check-doc-c.ts: oracle requires auth.otac_ttl_ms = 300_000 and lock window = 900_000.
- tests/contract/vnext-defaults.test.ts: oracle requires otac_ttl_ms = 300_000 and explicitly identifies older 10–15 minute prose as superseded by final DOC-C.

## Repair diff review

Commit a363fdb7b8ced513303f3e67ba4520dfcc1e9903 is scoped to the six declared target files and restores the Final DOC-C value without changing the 15-minute brute-force lock window.

## Verdict

VERDICT: PASS_SCOPED_HEAD_REVERIFY
ACTIONABLE_GAP_IN_THIS_SCOPE: 0
SOURCE_MUTATION_BY_THIS_REVIEW: NONE
UPSTREAM_NEXY_AI_MUTATION: NONE

## Test/evidence boundary

This record is a source/spec/diff reverify, not a substitute for executable exact-head CI.
GitHub Actions run 37240273646 attempt 4 remains EXECUTION_INFRA_FAILURE because first-wave jobs completed with zero executable steps. Therefore no global test PASS is claimed and project closure remains false.
