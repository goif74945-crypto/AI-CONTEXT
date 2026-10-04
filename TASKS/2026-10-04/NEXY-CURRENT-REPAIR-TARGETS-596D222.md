TASK_ID: NEXY-CURRENT-REPAIR-TARGETS-596D222-20261004
mode: AUDIT/CROSS/READ_ONLY
target_repo: goif74945-crypto/NEXY.AI-
target_branch: NEXY.ai
verified_head: 596d2225676ea978dc0ccf22e34a597949104f79
title: Current systems requiring repair or completion
claims:
- Runtime determinism: REPAIR_REQUIRED; authoritative Core currentTick uses process.hrtime.bigint() while canonical spec forbids Core system/monotonic clock access.
- Runtime enforcement: REPAIR_REQUIRED; static determinism checker detects process.hrtime/localeCompare but scans only packages/phase-f/game, excluding packages/core.
- Test / CI gate: REPAIR_REQUIRED; exact-head workflow runs 37202785747, 37202785787, 37202785862, 37202785871 all completed with conclusion=failure; no newer run found for this SHA.
- Exact-head deployment evidence: REPAIR_REQUIRED/BLOCKED; deploy/release evidence cannot be accepted while exact-head CI gate fails.
- G14 Toolchain / game WebGPU runtime: INCOMPLETE; packages/phase-f/game/runtime/webgpu.ts explicitly identifies itself as a stub/in-process simulation.
- localeCompare paths in L1o/Lo3/Sovereign remain NOT_VERIFIED risk, not classified as failure without host-independence proof.
status: PARTIAL / RELEASE_BLOCKED
whole_project_completion: NOT_PROVEN
sanitization: no secrets or sensitive PII
