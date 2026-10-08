# LEDGER 20261009-NEXY-GPT6-SOL-RAILWAY-LOOP-V1
| ID | SOURCE | OBSERVATION/CLAIM | PROOF LEVEL | VERDICT |
|---|---|---|---|---|
| S01 | GitHub NEXY.AI-/NEXY.ai branch API | observed HEAD 90fac4835788e867559858fc92d093ded3dcb1eb | live direct | VERIFIED_AT_OBSERVATION |
| S02 | GitHub AI-CONTEXT/main branch API | observed before writes HEAD f4bfedb910068f904607594c5e5107756af316b6 | live direct | VERIFIED_AT_OBSERVATION |
| S03 | Railway list_projects | project NEXY Validation R2 ID 01537473-6a6d-42a0-856f-40d8a4e6a712 exists | live direct | VERIFIED |
| S04 | Railway describe_environment | only observed environment production ID 776c1d3d-20f2-4b9f-9f07-8387ea9e63b8 isEphemeral false, staged null | live direct | VERIFIED |
| S05 | Railway describe_environment | nexy-e7-postgres and nexy-e7-redis latest deployments SUCCESS | live direct | SERVICE_LAUNCH_ONLY |
| S06 | Railway describe_service | nexy-validation connected NEXY.ai pinned old 9e615b04..., latest build FAILED, DATABASE_URL variable exists by name | live direct | VERIFIED_RESOURCE_NOT_CURRENT_HEAD |
| S07 | Railway deployment logs | old validation build reports Unicode parse/Phase-F scope failed | historical logs | VERIFIED_HISTORICAL_ONLY |
| S08 | Railway deployment logs | old branch validation failed auth/logout coverage tests | historical logs | VERIFIED_HISTORICAL_ONLY |
| S09 | Railway create_project attempt | Free plan resource provision limit exceeded | real tool error | BLOCKED_ACTION_PROVISION |
| S10 | Product Dockerfile at observed HEAD | runs cargo and Node tests in build, expects pinned tested head variables | GitHub file read | VERIFIED_SOURCE_ONLY |
| S11 | COMMANDS/20261009-NEXY-GPT6-SOL-RAILWAY-LOOP-V1.md | integrated Railway isolation+alternate runner+real test+feature extraction+checkpoint/safety | GitHub file readback + 26/26 checks | VERIFIED_COMMAND_ONLY |
OUTSTANDING: No Railway test against NEXY.ai HEAD 90fac... in this task, no real PG/Redis G3, full DOCX atomic inventory absent, no releases authorized by test-command creation.
