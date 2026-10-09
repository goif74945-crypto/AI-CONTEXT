# 20261009-NEXY-EX016-DIRECT-SPEC-CODE-AUDIT
MODE: ตรวจ / READ_ONLY_PRODUCT / FIRST_PARTY_SPEC_AND_SOURCE_ONLY
GOAL: Independently examine original DOCX and live NEXY.ai GitHub source, execute real scoped negative tests, enumerate actual progress and justified limited %.
AUTHORITATIVE_INPUT: attached แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx, locally recomputed SHA256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7; 12537 paragraphs, 10979 nonempty.
PRODUCT: goif74945-crypto/NEXY.AI-/NEXY.ai HEAD 8ed9af89f68fb82f60d4a4f5ccbc06005ce91992, tree 1087 entries/884 Git blobs.
CONTROL: goif74945-crypto/AI-CONTEXT/main is ONLY RECORD DESTINATION; its prior records are NOT product evidence.
PROVENANCE: GitHub fetch exact source files and tree; local original DOCX Python parse; locally git hash-object verified byte-for-byte reconstructed canonical-json.ts; native Node22 test executed.
SCOPE: 143 explicit source/evidence checks covering 26 defaults, 4 statuses, 8 states, 29 errors, 19 FSM transition contracts, 12 API exports, 12 screen mappings, 14 named components, 7 storage uniqueness constraints and 12 E-pack docs. Not exhaustive atomic features. Additional source reviewed SWARM, JUDGE, LAW, OTAC/auth, Queue, Storage, OBS, UI.
RUNTIME TEST: Node22 --experimental-strip-types on exact canonical Git blob: 10 tests / 4 pass, 6 fail; exit1. Scope intentionally negative.
OTHER TESTS: current-head GitHub Actions four workflows jobs reported 0 executable steps; no current-head full Vitest, browser E2E, real PG/Redis, Rust cargo executed in EX016.
RISKS: current source Canonical JSON mishandles sparse arrays/nonplain/side-effects; caller impact; DOC-E E01-E12 stale/blocked for old commit; User.email vs emailHash unique structural equivalence requires verification. Runtime conformance unknown.
ARTIFACTS: EVIDENCE/20261009-NEXY-EX016-DIRECT-SPEC-CODE-AUDIT-143-DIRECT-MATRIX.md and independent local file NEXY-EX016-DIRECT-SPEC-CODE-AUDIT.md with 143 rows, raw RED log.
CHANGES_PRODUCT: NONE. ROLLBACK: Not needed on Product; Control record forward-revert only if corrected.
ACCEPTANCE: actual source-inventory and source-specific match ratios with separate unavailable completion, no fake 100%; six failed negative tests accurately surfaced.
FINAL_STATUS: PARTIAL_FOR_FULL_PROJECT, VERIFIED_WITH_LIMITS_FOR_SOURCE_SUBSETS.
NEXT: Builder fixes canonicalJson with consumer regressions and real Vitest; auditor needs systematic complete atomization and current-head runtime tests.
TIMESTAMP_SOURCE: 2026-10-09 user local date.
