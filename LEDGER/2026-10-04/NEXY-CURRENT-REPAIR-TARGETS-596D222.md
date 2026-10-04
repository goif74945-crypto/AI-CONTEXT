LEDGER_ID: NEXY-CURRENT-REPAIR-TARGETS-596D222
head: 596d2225676ea978dc0ccf22e34a597949104f79
L1: canonical spec says Core cannot read system clock; monotonic_clock forbidden.
L2: packages/core/tick.ts blob 92ce2ae30a74d767013b322dd0d7aceb3fedd8b0 calls process.hrtime.bigint() at lines 41,58,108,139.
L3: scripts/check-static-determinism.ts blob 478c50115761d8f41d53383785531e7f8b19990b detects process.hrtime and localeCompare but walks only packages/phase-f/game.
L4: packages/phase-f/game/runtime/webgpu.ts blob 73773fa3a309d5dae0240fbf1dcdce9cc88aefb6 declares WebGPU pipeline stub/in-process simulation.
L5: exact-head GitHub Actions current query returns four runs, all failure, no newer rerun.
verdict: PARTIAL / RELEASE_BLOCKED
