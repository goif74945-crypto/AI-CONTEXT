# Defect Log

## D-001 — Immutable result contract violated on UNKNOWN branches

**Discovered by:** adversarial/property expansion after the initial 37-test suite passed.  
**Affected modules:** BKR and STCE.  
**Observed failure:** BKR `TemporalResolution` and STCE `TermResolution` dataclasses declared tuple-valued immutable fields, but `UNKNOWN` paths constructed them through `**payload` where payload values were mutable lists.

### Why it mattered
The main semantic status was correct, but downstream deterministic hashing, caching, equality assumptions, or callers relying on the declared immutable contract could observe a different runtime type on failure paths. A “mostly typed” contract is how quiet integration defects acquire office space.

### Root cause
Serialization payload representation (lists for canonical JSON) was reused directly as the runtime domain-object constructor.

### Repair
Separated the canonical fingerprint payload from the runtime object construction. Runtime fields are now explicit tuples on UNKNOWN/CONFLICT/PASS paths while fingerprint payloads retain JSON arrays.

### Regression proof
- new `tests/test_properties.py::TestContractTypes` checks failure-path tuple contracts;
- algebraic and input-order invariance tests were added at the same time;
- full regression suite after repair: 47 tests PASS;
- static compile after repair: PASS.

## Remaining known design limitations
No production integration, distributed transport, persistence engine, cryptographic signing, real NEXY adapter, deployment, or load/SLA proof is claimed.

## D-002 — Guard metric direction was implicitly lower-is-better

**Discovered by:** design audit after D-001 repair, before evidence sealing.  
**Affected module:** CUVL.  
**Observed design gap:** `guard_regression = candidate_guard - baseline_guard` treated every guard metric increase as harmful. This is correct for latency/error-rate style guards but wrong for higher-is-better guards such as safety success or availability.

### Repair
Added explicit `guard_direction: Direction` to `ValueContract`, validated the enum type, and normalized regression so positive values always mean degradation regardless of metric direction.

### Regression proof
Added `test_higher_is_better_guard_detects_downward_regression` and invalid-direction rejection. Full suite after repair: 49 tests PASS.

## D-003 — First remote publication of merge lattice was semantically equivalent but byte-different

**Discovered by:** publication identity gate before completion.  
**Affected artifact:** remote `src/lo4lab/merge_lattice.py` only.  
**Observed failure:** an intermediate publication serialized the locally tested implementation into a compact equivalent form. Functional intent was preserved, but the Git blob was not the exact tested artifact, so the evidence contract failed.

### Repair
Fetched the remote blob SHA, replaced the file with the exact locally tested content, then re-fetched the remote blob and compared it with local `git hash-object`.

### Regression / identity proof
Final remote blob `226992443ef4b27b38deea9ed430abbf847d28d9` exactly matches the local tested file. The final identity gate matches all 15 source+test files.
