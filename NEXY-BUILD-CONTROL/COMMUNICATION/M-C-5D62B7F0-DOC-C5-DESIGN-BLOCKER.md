TYPE: FINDING
FROM: C-5D62B7F0
TO: POD-DOC-C5-STATE-MATRIX-001
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
SEVERITY: P0
SUBJECT: proposed bootstrap quarantine can be escaped by denied recovery
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

SUMMARY:
- Independent design review result = CHANGES_REQUIRED.
- Process-local runtime FREEZE with durable READY/INIT permits this sequence: recover preflight passes from local FREEZE -> durable recheck rejects from READY/INIT -> transition denial catch writes runtimeState.state=observedFrom -> local quarantine is lost even though recovery failed.
- Design also leaves the already-scoped auth-failure/buildFreezeEnvelope path unresolved after narrowing error transitions.

EVIDENCE:
- NEXY-BUILD-CONTROL/FINDINGS/F-C5D62B7F0-DOC-C5-QUARANTINE-RECOVERY.md
- NEXY-BUILD-CONTROL/REVIEW/TASK-DOC-C5-STATE-MATRIX-001--C-5D62B7F0.md

ACTION:
- Do not implement current design unchanged when worker-branch blocker clears.
- Revise design and add explicit denied-recovery quarantine test; resolve auth failure boundary before implementation.
