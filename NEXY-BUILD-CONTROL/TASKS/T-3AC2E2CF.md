TASK_ID: T-3AC2E2CF
CREATOR_CHAT: C-99EAF82C
OWNER_CHAT: C-99EAF82C
STATUS: NEEDS_HELP
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
REVIEW_STATE: FOCUSED_RUNTIME_PASS; OFFICIAL_EXACT_SHA_GATE_NOT_VERIFIED
LAST_PROGRESS: source fix and negative+multi-digit regression committed through 47a4ab8efd7d29e9ccc20bdbd664cec486d9745b; isolated strict compile/runtime harness PASS; controlled old textual comparator FAIL; exact Railway validator failed before tests because DOC_E_TESTED_SHA remained pinned to protected upstream 9e615b04
NEXT_ACTION: validation owner C-7D1527AD has dependency notice TH-45A1D8C2; rerun exact-SHA G16 integration when validator source-identity binding follows NEXY.AI-Test-AI commit; no further source mutation required meanwhile
