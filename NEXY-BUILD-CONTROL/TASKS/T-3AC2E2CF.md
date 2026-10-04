TASK_ID: T-3AC2E2CF
CREATOR_CHAT: C-99EAF82C
OWNER_CHAT: C-99EAF82C
STATUS: IMPLEMENTING
PRIORITY: P2
RISK: MEDIUM
BASE_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
TARGET_PATHS:
- packages/phase-f/game/world-partition.ts
- tests/integration/g16-world-partition.spec.ts
SEMANTIC_SCOPE: Align G16 world-state chunk hashing with the authoritative integer tuple canonical chunk order; add regression proof for multi-digit and negative chunk coordinates. No activation-metric invention and no unrelated game changes.
DEPENDENCIES:
- Authoritative Spec G16 World Partition Index Law and World State Hash Law
BLOCKS: none
TEST_PLAN:
- add regression that distinguishes numeric tuple ordering from string ChunkID ordering
- run targeted G16 integration test if executable environment is available
- otherwise preserve source-level evidence and do not claim PASS
REVIEW_STATE: NOT_STARTED
LAST_PROGRESS: source/spec inspection identified canonical-order inconsistency in worldStateHash
NEXT_ACTION: refresh work HEAD, patch comparator use, add regression test, verify
