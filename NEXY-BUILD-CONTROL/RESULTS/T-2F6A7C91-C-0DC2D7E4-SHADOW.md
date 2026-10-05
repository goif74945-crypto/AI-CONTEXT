RESULT_TYPE: RED_TEAM_TEST_RESULT
RESULT_ID: R-0DC2D7E4-CAPABILITY-DEPTH
CHAT_ID: C-0DC2D7E4
TASK_ID: T-2F6A7C91
CORROBORATES_FINDING: F-E4C19A73-04
REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.AI-Test-AI
COMMIT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_PATH: packages/phase-f/universe/capability-node.ts
SOURCE_BLOB_SHA: 25d26bf233b1d7b446027aad391688b7e91b09a0
SPEC_FILENAME: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SPEC_HASH_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_EVIDENCE:
- lines 7473-7505: Capability Graph requires No cycles, MaxDepth <= 5, No escalation upward, No forbidden collision.
- lines 7621-7653: G21 Gate A requires deterministic Dependency closure resolution and no bypass.
RUNNER: Node.js v22.16.0 isolated executable shadow harness
COMMAND: node /mnt/data/capability_depth_redteam.js
RESULT: COUNTEREXAMPLE_REPRODUCED
EXIT_CODE: 0

FACT:
Current depthOf() uses a global visited set and returns 0 for any previously completed dependency subtree. That is not a valid depth cache.

COUNTEREXAMPLE_GRAPH:
candidate -> [A,B]
A -> C
B -> X
X -> C
C -> D
D -> E
E -> F

OBSERVED_EXECUTABLE_OUTPUT:
dependency_order=[A,B] buggy_depth=5 correct_depth=6 buggy_accepts_max5=true correct_accepts_max5=false
dependency_order=[B,A] buggy_depth=6 correct_depth=6 buggy_accepts_max5=false correct_accepts_max5=false

IMPACT:
The same shared DAG can be accepted or rejected solely from dependency traversal order. With [A,B], a true depth-6 graph passes the MaxDepth<=5 check. This is an admission bypass and deterministic-verifier defect.

EVIDENCE_CLASS:
Independent executable model of the exact current depthOf control-flow, plus direct source inspection. This is not claimed as an exact-module Vitest execution because the current runtime checkout is not locally materialized.

RECOMMENDED_REPAIR:
Replace completed-node visited=>0 behavior with memoized subtree depth keyed by capabilityNodeKey. Preserve visiting as the cycle detector. Add regression vectors for both dependency orders and require identical rejection.

SOURCE_MUTATION_BY_THIS_CHAT: NONE
