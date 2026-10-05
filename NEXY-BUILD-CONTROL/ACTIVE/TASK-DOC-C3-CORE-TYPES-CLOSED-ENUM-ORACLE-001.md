TASK_ID: TASK-DOC-C3-CORE-TYPES-CLOSED-ENUM-ORACLE-001
OWNER_CHAT: C-SOL-20261006-0132
STATUS: IMPLEMENTING_TEST_ORACLE
PRIORITY: P1
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
PROTECTED_BRANCH: NEXY.ai
REQ_ID: REQ-DOC-C-3-1-CORE-TYPES
FINDING_ID: FINDING-DOC-C3-CORE-TYPES-CLOSED-ENUM-ORACLE-GAP-001
SEMANTIC_SCOPE: Add isolated exact-set and schema-rejection contract coverage for canonical SystemStatus and SystemState enums.
TARGET_PATHS:
- tests/contract/core-types-closed-enums.test.ts
REQUIRED:
- SystemStatus exact set = OK, DEGRADED, FREEZE, STOP
- SystemState exact set = INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP
- both schemas reject representative unsupported additions
FORBIDDEN:
- no mutation of state transition runtime or existing state-matrix test
- no NEXY.ai mutation
CONFLICT_AVOIDANCE: active state-transition owners keep their files; this task adds a standalone contract oracle only.
