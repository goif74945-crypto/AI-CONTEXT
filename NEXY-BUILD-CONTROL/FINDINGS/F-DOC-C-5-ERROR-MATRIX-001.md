# F-DOC-C-5-ERROR-MATRIX-001

STATUS: OPEN
REQ_ID: DOC-C-5.2-ERROR-TRANSITIONS
TASK_ID: TASK-DOC-C-5-ERROR-MATRIX-20261005T1920Z0700
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P1
OBSERVED:
- packages/core/vnext-state-matrix.ts contains error -> FREEZE rows for INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE.
- tests/contract/state-matrix.test.ts asserts that broader set as "final DOC-C".
- packages/api/bootstrap.ts uses error/CORE as a pre-admission INIT failure path.

EXPECTED:
FINAL DOC-C §5.2 lists error -> FREEZE for RUNNING and VERIFYING only. Bootstrap fail-closed handling must not manufacture a legal INIT error transition.

SPEC_EVIDENCE:
Authoritative locked spec SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7; FINAL DOC-C §5.2 and §5.6.

REPRODUCTION:
Inspect NEXY.AI-Test-AI@608426cb30398b1f3461866f7079d2a435c96b96:
- packages/core/vnext-state-matrix.ts
- tests/contract/state-matrix.test.ts
- packages/api/bootstrap.ts

STATUS_NOTE:
Repair is blocked by F-CONTROL-WORKER-REF-NAMESPACE-001; source has not been mutated.
