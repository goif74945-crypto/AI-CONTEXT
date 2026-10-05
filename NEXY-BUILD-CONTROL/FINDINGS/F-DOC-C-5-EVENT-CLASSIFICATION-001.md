# F-DOC-C-5-EVENT-CLASSIFICATION-001

STATUS: OPEN
SEVERITY: P2
CLASS: CONTRACT_DRIFT / TEST_ORACLE_DEFECT
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

OBSERVED:
- FINAL DOC-C section 5.1 includes `timeout` and `cancel` in the canonical `SystemEvent` union.
- TypeScript `tests/contract/state-matrix.test.ts` excludes `timeout` and `cancel` from `DOC_C_FINAL_EVENTS` and labels them compatibility rails.
- `packages/core/vnext-state-matrix.ts` comments also describe cancel/timeout as extended compatibility rails even though runtime retains them.

EXPECTED:
Required DOC-C events must be classified and tested as required canonical events, not optional compatibility behavior.

IMPACT:
Runtime behavior currently retains the events, but the test/documentation oracle misstates authority and can permit future required-behavior removal under a false compatibility assumption.

BLOCKED_BY: F-CONTROL-WORKER-REF-NAMESPACE-001
