# LEDGER-NEXY-DOC-E-2026-09-30-EFC680A

| id | source | claim | proof | deps | risk | status | confidence | freshness |
|---|---|---|---|---|---|---|---|---|
| L1 | design DOCX | full DOC-E source authority was read before mutation | SHA b35ee1bf...; 12,537 logical lines; 32/32 ranges; no gaps | source extraction | high | VERIFIED | 1.00 | current-task |
| L2 | GitHub | isolated DOC-E source HEAD | e82edcd9e6ab1322526499a45ecb72ff9a487e4a / tree 5cc36e3b85e775c462c4a2baf6a05abe7150f049 | work/doc-e-exact-head-20260930 | high | VERIFIED | 1.00 | current |
| L3 | Railway build | exact-head static/contract/web validation works on provider plane | validation image generated Prisma, installed Rust, typechecked, ran contracts, built web, verified apps/web/.next/BUILD_ID | Railway builder | high | VERIFIED | 1.00 | current |
| L4 | Railway runtime | E3 migration roundtrip passes on isolated PostgreSQL | final campaigns reached post-E3 gates; migration runner fail-closed | PostgreSQL | high | VERIFIED | 1.00 | current |
| L5 | Railway runtime | E7 queue readiness passes through production API/Redis/BullMQ/worker path | final campaigns complete E7; canonical ULID/auth fixture; provider run continues beyond E7 | PostgreSQL + Redis + web + worker | high | VERIFIED | 1.00 | current |
| L6 | Railway runtime | E8 monitoring verification passes | six NEXY_ALARM_EXTERNAL classes emitted to sink_id railway:nexy-validation-branch | provider log sink | high | VERIFIED | 1.00 | current |
| L7 | Railway runtime | E9 incident lifecycle passes | full campaign reaches E10 after E9; production-path freeze/recovery drill + evidence validator | PostgreSQL + recovery API | high | VERIFIED | 1.00 | current |
| L8 | Railway rollback | application rollback executed successfully | deployment 367ffe4d-794d-4d10-8c2d-e4573c6afb8a on SHA 45ec2284... = SUCCESS; E1-E9 incl. E8 PASS | validation service | high | VERIFIED | 1.00 | current |
| L9 | Railway restore | current release restored successfully after rollback | deployment db54cf4f-55ae-4218-acdb-840225a2fd05 on SHA e82edcd9... = SUCCESS; E1-E9 incl. E8 PASS | validation service | high | VERIFIED | 1.00 | current |
| L10 | E10 provider receipt | provider deploy/rollback commands are bound to current exact head | deploy_command_id db54cf4f...; rollback_command_id 367ffe4d...; final E10=PASS | Railway proof | high | VERIFIED | 1.00 | current |
| L11 | E12 provider receipt | application rollback execution proof is current and separate from E3 | final E12=PASS using real rollback deployment + health/smoke/monitoring proof | Railway proof | high | VERIFIED | 1.00 | current |
| L12 | final DOC-E attestation | E1-E10 PASS, E11 BLOCKED_EXTERNAL, E12 PASS | deployment 46542beb-fefb-4745-a217-42f546a103ab | exact SHA/tree | critical | VERIFIED | 1.00 | current |
| L13 | final DOC-E attestation | evidence root integrity | 3da765cb2c0123c9b718dc1f38bd16273bb03f1eba20ea9ab015cb06c774ad85 | E1-E12 records | high | VERIFIED | 1.00 | current |
| L14 | final DOC-E attestation | attestation artifact integrity | d816e1053143e373b71b6e921ebb6b2378b3dacbff5d480cd61913972033b3a1 | final campaign | high | VERIFIED | 1.00 | current |
| L15 | E11 verifier | external signoff is missing | no valid engineering/security/migration approval receipt supplied | external actors | S4 | BLOCKED_EXTERNAL | 1.00 | current |
| L16 | release gate | release and deploy are not authorized | release_authorized=false; deploy_authorized=false; blocking_reasons=[E11:BLOCKED_EXTERNAL] | E11 | S4 | VERIFIED_BLOCK | 1.00 | current |
| L17 | Git branch boundary | NEXY.ai was not modified by this isolated DOC-E batch | implementation remains on work/doc-e-exact-head-20260930 | concurrent-work isolation | medium | VERIFIED | 1.00 | current |
