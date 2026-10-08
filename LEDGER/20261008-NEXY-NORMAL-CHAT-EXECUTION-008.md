# LEDGER 20261008-NEXY-NORMAL-CHAT-EXECUTION-008
| ID | Claim | Source/proof | Status |
| --- | --- | --- | --- |
| 008-001 | Observed product NEXY.ai HEAD 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08 | GitHub branch API | VERIFIED_AT_OBSERVATION |
| 008-002 | AI-CONTEXT main had committed 007 evidence at fc7dc9570cbe2d3a9a287db1c2613b1f97739cb7 | GitHub branch API, commit file list, file readbacks | VERIFIED |
| 008-003 | Model 007 contains five test cases but no real DB/Redis integration | EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS-model.test.cjs | VERIFIED_SOURCE; EXECUTION_CLAIM_FROM_PRIOR_WORKER_ONLY |
| 008-004 | Queue source race is a candidate source-reachable terminal overwrite | product dispatch.ts source observation recorded in 006/007 at 44bcb851 | VERIFIED_SOURCE_WITH_LIMITS, NO_PRODUCTION_INCIDENT_PROOF |
| 008-005 | CAS alone cannot certify Redis enqueue-before-durable-transition correctness | product jobs.ts/dispatch.ts/workers.ts cross-boundary analysis | DESIGN_REQUIREMENT |
| 008-006 | Linux cage has unisolated direct-spawn fallback when bwrap unavailable | product cage.ts source observed in 006/007 | VERIFIED_SOURCE_RISK, NO_PROD_EXPLOIT_PROOF |
| 008-007 | Five named GitHub Actions workflow runs failed on observed product HEAD | GitHub /actions/runs/{id} GET for five run IDs | VERIFIED_AT_OBSERVATION |
| 008-008 | Exact-head and E7 jobs checked were pre-step failures, runner_name empty | GitHub /runs/37741650349/jobs and /runs/37741650376/jobs | VERIFIED_BOUNDED |
| 008-009 | Cause of CI pre-step failure cannot be assigned to YAML, billing, quota, or policy without further evidence | bounded GitHub jobs/run evidence | UNKNOWN |
| 008-010 | Instruction 008 written and requires repo-integrated tests or real patch candidate | COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-008.md and read-back | VERIFIED_COMMAND_ONLY |
RELEASE_STATUS: NOT_AUTHORIZED. PRODUCT_CODE_CHANGED: NO in this task. LIMIT: No tests on NEXY code executed by command author.
