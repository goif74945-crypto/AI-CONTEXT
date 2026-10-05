TASK_ID: TASK-GLOBAL-API-OWNER-RECOVERY-AUTHORITY-001
OWNER_CHAT: C-SOL-20261006-P0-OWNER-RECOVERY
STATUS: ACTIVE
PRIORITY: P0
BASE_SHA: 0440c47f14dadb1a4fb4bcdd3fd53d7bb9fce6c9
SEMANTIC_SCOPE: remove/disable unauthorized sessionless owner-recovery mutation surface; do not invent a new exemption
TARGET_PATHS:
- apps/web/app/api/auth/owner-recovery/route.ts
- packages/api/owner-recovery.ts
- packages/contracts/auth.ts
- tests/coverage/owner-recovery-control-plane.test.ts
WORKER_BRANCH: NEXY.AI-Test-AI-work/TASK-GLOBAL-API-OWNER-RECOVERY-AUTHORITY-001
