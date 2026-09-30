# LEDGER-NEXY-DOC-E-2026-09-30-EFC680A

| id | source | claim | proof | deps | risk | status | confidence | freshness |
|---|---|---|---|---|---|---|---|---|
| L1 | design DOCX | full DOC-E authority read before mutation | SHA b35ee1bf...; 12,537 logical lines; 32/32 ranges; no gaps | source extraction | high | VERIFIED | 1.00 | current-task |
| L2 | GitHub | isolated DOC-E exact head | e82edcd9e6ab1322526499a45ecb72ff9a487e4a / tree 5cc36e3b85e775c462c4a2baf6a05abe7150f049 | work/doc-e-exact-head-20260930 | high | VERIFIED | 1.00 | current |
| L3 | Railway build | exact-head static/contracts/web build passed | Prisma generated; Rust stable; typecheck; full contract suite; build:web; apps/web/.next/BUILD_ID | Railway builder | high | VERIFIED | 1.00 | current |
| L4 | Railway runtime | E3 migration roundtrip passes | final current-head campaign E3 PASS | PostgreSQL | high | VERIFIED | 1.00 | current |
| L5 | Railway runtime | E7 queue readiness passes production boundary | current-head campaigns complete API -> Redis/BullMQ -> worker proof | PostgreSQL + Redis + web + worker | high | VERIFIED | 1.00 | current |
| L6 | Railway runtime | E8 monitoring passes | six canonical NEXY_ALARM_EXTERNAL classes emitted to railway:nexy-validation-branch | provider log sink | high | VERIFIED | 1.00 | current |
| L7 | Railway runtime | E9 incident lifecycle passes | current-head full campaign continues through E10 and final attestation | PostgreSQL + recovery API | high | VERIFIED | 1.00 | current |
| L8 | Railway rollback | application rollback executed successfully | d16a8141-365d-4408-ab9e-4ab2ea05ac5b -> SHA 45ec2284... = SUCCESS; E1-E9 PASS | validation service | high | VERIFIED | 1.00 | current |
| L9 | Railway restore | current exact head restored successfully | 8d6180ec-1a6e-4fab-9c3d-19da8daf1ba6 -> SHA e82edcd9... = SUCCESS | validation service | high | VERIFIED | 1.00 | current |
| L10 | E10 receipt | deploy/rollback mechanism bound to current exact head | deploy 227a6752...; rollback d16a8141...; final E10 PASS | Railway proof | high | VERIFIED | 1.00 | current |
| L11 | E12 receipt | application rollback proof separate from E3 | final E12 PASS; health/smoke/monitoring verified by real rollback target campaign | Railway proof | high | VERIFIED | 1.00 | current |
| L12 | final attestation | E1-E10 PASS, E11 BLOCKED_EXTERNAL, E12 PASS | deployment 8d6180ec-1a6e-4fab-9c3d-19da8daf1ba6 | exact SHA/tree | critical | VERIFIED | 1.00 | current |
| L13 | final attestation | evidence root integrity | 9fb0c7cf13d920a2dededd4ac90e39d66b7f6716d4c7cb733d700502d3a02465 | E1-E12 records | high | VERIFIED | 1.00 | current |
| L14 | final attestation | attestation artifact integrity | a8082bc1386cd5cb8f8c62fcf10fdd8a2082b02d13b05578d42f97e6437e5d8a | final campaign | high | VERIFIED | 1.00 | current |
| L15 | E11 verifier | authorized external signoff missing | no valid engineering/security/migration approval receipt supplied | external actors | S4 | BLOCKED_EXTERNAL | 1.00 | current |
| L16 | release gate | release/deploy remain unauthorized | release_authorized=false; deploy_authorized=false; blocker E11 only | E11 | S4 | VERIFIED_BLOCK | 1.00 | current |
| L17 | canonical branch | NEXY.ai is the sole source-of-truth/default branch | default_branch=NEXY.ai; merge 6c53f51a...; cleanup d7f824ed... | GitHub refs | high | VERIFIED | 1.00 | current |
| L18 | supersession | older DOC-E campaign IDs/hashes in v1 are historical, not latest truth | latest final deployment 8d6180ec... and hashes L13-L14 supersede conflicting v1 current-state fields | AI-CONTEXT v2 | medium | VERIFIED | 1.00 | current |

| L19 | merge analysis | concurrent NEXY.ai and DOC-E edits did not overlap paths | 7 main-side files vs 41 DOC-E files; intersection=[] | merge base 0f9c8c65... | high | VERIFIED | 1.00 | current |
| L20 | merged tree | main-side blobs and DOC-E blobs preserved byte-for-byte | merged tree a7e98a1f...; both mismatch sets empty | Git trees | high | VERIFIED | 1.00 | current |
| L21 | canonical cleanup | workflow/runtime evidence now names NEXY.ai | cleanup commit d7f824ed7f4b70e5308f3b8bb6a31fbf1ad0a61e / tree 4cf698ed... | NEXY.ai | high | VERIFIED | 1.00 | current |
| L22 | post-merge validation | fresh current-head validation is executing | Railway deployment 09da96e1-f989-43d4-9e5e-3001b5e36335 status BUILDING at write time | Railway | high | PENDING | 1.00 | current |
