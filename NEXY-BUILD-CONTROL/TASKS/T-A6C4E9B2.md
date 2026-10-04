TASK_ID: T-A6C4E9B2
CREATOR_CHAT: C-7B5E20D1
OWNER_CHAT: C-7B5E20D1
STATUS: IMPLEMENTING
PRIORITY: P1
RISK: MEDIUM
BASE_SHA: cf8b517975b252575fde4d4b155d18e56df82a73
EXPECTED_PARENT_SHA: cf8b517975b252575fde4d4b155d18e56df82a73
TARGET_PATHS:
- core-kernel/src/kernel/vnext_matrix.rs
SEMANTIC_SCOPE: Align Rust VNext TRANSITIONS and Rust unit oracle to the authoritative final DOC-C §5.2/§5.4 transition set after TypeScript exactness fix 27af7f; remove only the five superseded non-active error->FREEZE edges. No TypeScript state matrix, hydration, persistence, event ownership, guard, error taxonomy, or protected-branch changes.
DEPENDENCIES:
- authoritative DOCX FINAL VERDICT / DOC-C build authority
- final DOC-C executable matrix P10353-P10452
- TypeScript matrix commit 27af7f93893c7589e516c269fae41aa467c2cdb9
- Railway executable failure deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
BLOCKS:
- Rust/TypeScript final DOC-C parity contract
TEST_PLAN:
- verify exact Rust TRANSITIONS equals current TypeScript VNEXT_TRANSITIONS
- Rust unit oracle: RUNNING/VERIFYING error->FREEZE; INIT/READY/CONSENSUS/STABLE/FREEZE error => NoSuchTransition
- rely on fresh exact-head Railway test:contract / core-kernel test execution after commit
- do not claim full PASS without exact-head execution
REVIEW_STATE: NOT_STARTED
LAST_PROGRESS: Railway exact work-branch execution proved 5 obsolete Rust error edges remain after TS final-DOC-C correction.
NEXT_ACTION: Recheck work HEAD/file blob, apply one-file repair, then observe exact-head executable validation.
