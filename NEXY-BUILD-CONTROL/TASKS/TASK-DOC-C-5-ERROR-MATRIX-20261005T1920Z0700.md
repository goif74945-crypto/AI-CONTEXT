# TASK-DOC-C-5-ERROR-MATRIX-20261005T1920Z0700

STATUS: BLOCKED
BLOCK_CLASS: EXTERNAL_TRUE_BLOCK
PROJECT: NEXY.AI / NEXY-IGNIS
EPOCH_ID: EPOCH-20261005-b35ee1bf-608426cb
SPEC_ID: NEXY-IGNIS-b35ee1bf82125792
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_REPOSITORY: goif74945-crypto/NEXY.AI-
INTEGRATION_BRANCH: NEXY.AI-Test-AI
INTENDED_WORKER_BRANCH: NEXY.AI-Test-AI/work/TASK-DOC-C-5-ERROR-MATRIX-20261005T1920Z0700
EXPECTED_PARENT_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
REQ_ID: DOC-C-5.2-ERROR-TRANSITIONS
FINDING_ID: F-DOC-C-5-ERROR-MATRIX-001
BLOCK_FINDING_ID: F-CONTROL-WORKER-REF-NAMESPACE-001

OBSERVED:
- Runtime VNEXT_TRANSITIONS permits error -> FREEZE from INIT, READY, CONSENSUS, STABLE, and FREEZE in addition to RUNNING and VERIFYING.
- FINAL DOC-C §5.2 enumerates error -> FREEZE only for RUNNING and VERIFYING.
- bootstrap currently relies on INIT --error/CORE--> FREEZE for pre-admission dependency failure.
- tests/contract/state-matrix.test.ts encodes the unsupported broader error transition oracle.

EXPECTED:
- Legal FSM rows match FINAL DOC-C §5.2.
- Pre-admission bootstrap integrity failure remains fail-closed without redefining the legal FSM.

BLOCK:
- Worker branch creation using the mandated prefix failed with GitHub HTTP 422.
- Git ref hierarchy cannot contain refs/heads/NEXY.AI-Test-AI and refs/heads/NEXY.AI-Test-AI/work/<TASK> simultaneously because the former occupies the prefix path.

UNBLOCK_CONDITION:
- Explicitly change the worker branch naming law to a non-descendant namespace (example class only: work/NEXY.AI-Test-AI/<TASK> or NEXY.AI-Test-AI-work/<TASK>), OR
- Explicitly authorize direct mutation on NEXY.AI-Test-AI for this repair.
- Do not delete/rename NEXY.AI-Test-AI implicitly.
