TASK_ID: TASK-DOC-C3-API-HANDLER-STATE-INTEGRITY-001
OWNER_CHAT: C-SOL-20261006-0144-API-HANDLER-STATE
STATUS: ACTIVE
PRIORITY: P1
BASE_SHA: 586275e163d5f6503874621223cb89f878b3da37
SEMANTIC_SCOPE: generic web exception envelope must serialize authoritative runtime SystemState and never fabricate FREEZE
TARGET_PATHS:
- packages/api/runtime-state.ts
- apps/web/lib/api-handler.ts
- tests/contract/api-handler.test.ts
SCOPE_NOTE: API projection added because canonical module law forbids UI->CORE direct import; no state mutation is exposed.
WORKER_BRANCH: NEXY.AI-Test-AI-work/TASK-DOC-C3-API-HANDLER-STATE-INTEGRITY-001
