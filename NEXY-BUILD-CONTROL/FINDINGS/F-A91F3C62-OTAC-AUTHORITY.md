FINDING_ID: F-A91F3C62-OTAC-AUTHORITY
FROM_CHAT: C-7A2D91F4
TO_CHAT: C-7E4A91D2
TASK_ID: T-A91F3C62
HEAD_SHA: 6597a53485e78021ebbca61f9a8ecc74cb90c084
SEVERITY: P0

OBSERVATION:
T-A91F3C62 changed canonical OTAC validity from 5 minutes to 15 minutes by treating early TEMPORARY/Auth V0 prose as controlling authority. The same authoritative DOCX later defines DOC-C vNEXT canonical defaults with otac_ttl_ms = 300000 and §8.2 OTAC Policy TTL = 5 minutes. AI-CONTEXT current DOC-C normalization independently records OTAC TTL = 5 min and lock window = 15 min.

EXPECTED:
- VNEXT_DEFAULTS.auth.otac_ttl_ms = 300000
- Rust EXPIRY_TICKS = 300000000000 at 1 GHz
- brute-force lock window remains 900000 ms (15 min)
- tests/check-doc-c enforce the canonical 5-minute OTAC validity

ACTUAL:
- current work-branch packages/api/vnext-config.ts blob 0ff32485b01fdf39e895902757348df3c63118a1 sets otac_ttl_ms = 900000
- commit aab5bbd662b59f3c70976f970e9ee3708df826c2 changed Rust, TS config, check-doc-c, Prisma comment, and tests to 15-minute OTAC validity

REPRODUCTION:
1. Authoritative DOCX later DOC-C:
   - extracted lines 9586-9637: DOC-C vNEXT BUILD SPEC -> Canonical Defaults -> auth.otac_ttl_ms: 300000
   - extracted lines 8756-8762: OTAC Policy -> TTL = 5 minutes; lock window after max fail = 15 minutes
   - extracted lines 8179-8185 / 8218-8223: canonical config/value table -> otac_ttl_ms 300000; lock 900000
2. AI-CONTEXT projects/NEXY.AI/deep/doc-c-vnext-build-spec.md current canonical defaults: OTAC TTL = 5 min; lock window = 15 min.
3. Current NEXY.AI-Test-AI packages/api/vnext-config.ts: otac_ttl_ms = 900000.

EVIDENCE:
- authoritative spec: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
- AI-CONTEXT/projects/NEXY.AI/deep/doc-c-vnext-build-spec.md
- source commit aab5bbd662b59f3c70976f970e9ee3708df826c2
- current work head 6597a53485e78021ebbca61f9a8ecc74cb90c084
- current config blob 0ff32485b01fdf39e895902757348df3c63118a1

SUGGESTED_DIRECTION:
Restore only OTAC validity to DOC-C canonical 5 min while preserving separate 15-minute brute-force lock window; update affected tests/comments consistently and execute focused auth/default/check-doc-c verification.

STATUS: OPEN
