TASK_ID: T-UIEXPORT-5C2A91D7
OWNER_CHAT: C-SOL-20261006-UIEXPORT
STATUS: INTEGRATED_CI_BLOCKED
PRIORITY: P1

REQUIREMENT:
DOC-B §16.4 / DOC-D S5 directive-detail export must remain disabled while backend release is blocked.

MUTATION_SCOPE:
- apps/web/app/directives/[id]/page.tsx
- tests/contract/directive-export-truth-gate.test.ts

INTEGRATION:
- branch: NEXY.AI-Test-AI
- parent_sha: 0440c47f14dadb1a4fb4bcdd3fd53d7bb9fce6c9
- integrated_sha: 07017a0181b2abfb39db5d4618e6d2cf4cc98c54
- integration_mode: direct fast-forward commit after reviewed worker patch; force=false
- source_blob: 7d0768c969b6969e11c7fbd43ea6b5c2739b30ce
- test_blob: 68b5382c852ff379a1dffa22b6cfafa1a60cc5f8
- reviewed_worker_head: 8e4e42142649135c7110464edcf4738391fb6dcc
- refreshed_worker_head: 7b657a8e1f8f8e1de4988ce07c248c83a997c358
- pr: #39 (closed redundant after direct fast-forward integration)

IMPLEMENTED_BEHAVIOR:
- Export is enabled only when canonical backend result.releaseable === true.
- exportTruth() independently fails closed when release is not authorized.
- No API, LAW, auth, state-machine, Vault, or NEXY.ai mutation.

VERIFICATION:
- exact integrated source/test blob read-back: PASS
- focused executable source-contract assertions: PASS
- final integrated diff: 2 files only, +20/-3
- exact-head workflow 37360494478: FAILURE before exposed steps; artifacts=[]
- exact-head workflow 37360494472: FAILURE before exposed steps; artifacts=[]
- full-suite PASS: NOT CLAIMED
- code-failure inference from workflow status: FORBIDDEN; no step/log evidence exists.

BLOCKER:
Repository exact-head GitHub Actions infrastructure is failing before job-step evidence becomes available. Validation scope has active peer ownership, so this task does not duplicate that repair.

CONTINUATION_REQUIRED:
Independent exact-head CI rerun is still required once runner evidence is available, but implementation and integration of this requirement are complete.
