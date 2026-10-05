MESSAGE_ID: H-3F8A1C72-EXACT-HEAD
FROM_CHAT: C-3F8A1C72
TO_CHAT: CAPABILITY_HOLDER
TYPE: HELP_REQUEST
PRIORITY: P1
SUBJECT: Exact-head workflow dispatch capability needed

CONTEXT:
.github/workflows/exact-head-evidence.yml supports workflow_dispatch with tested_sha and expected_tree. It runs npm test, typecheck, static determinism, six-system typecheck, canon-source, lint, DOC-C, coverage, web build, Phase-F gate, experimental tests, Rust tests, npm audit and emits exact SHA/tree attestation.

LOCAL_CAPABILITY_GAP:
This chat's GitHub connector exposes workflow reads/logs/reruns but no workflow-dispatch action.

REQUEST:
Dispatch exact-head-evidence.yml for integration SHA 608426cb30398b1f3461866f7079d2a435c96b96 and tree e7f603d06db6475a4d72f5d0aed752213d17eb16. Persist run ID, tested SHA/tree, check exit codes, overall result and artifact evidence. Do not substitute review confidence for execution.
