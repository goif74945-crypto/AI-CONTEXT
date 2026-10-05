# F-PARITY-VNEXT-ERROR-TRANSITIONS-001

STATUS: OPEN
SEVERITY: P1
REQ_ID: DOC-C-5.2-ERROR-TRANSITIONS
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

OBSERVED:
- TypeScript `packages/core/vnext-state-matrix.ts` allows `error -> FREEZE` from INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE.
- Rust `core-kernel/src/kernel/vnext_matrix.rs` allows `error -> FREEZE` only from RUNNING and VERIFYING and explicitly tests rejection elsewhere.

EXPECTED:
Required cross-runtime mirrors must be semantically equivalent and match FINAL DOC-C section 5.2.

CLASS: PARITY_DEFECT
RELATED_FINDING: F-DOC-C-5-ERROR-MATRIX-001
BLOCKED_BY: F-CONTROL-WORKER-REF-NAMESPACE-001
