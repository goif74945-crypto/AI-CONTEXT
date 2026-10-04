# Failure -> Repair -> Re-test Ledger

## FR-001 — Incorrect Pareto test oracle

**Observed:** first suite executed 27 tests; `test_pareto_frontier_preserves_tradeoffs` failed because the test expected candidate `a` to dominate `c`.

**Root cause:** `a` had better latency but lower satisfaction than `c`; by Pareto definition it cannot dominate `c`. Candidate `b` was better in both dimensions and was the only valid dominator.

**Correction:** fixed the test expectation from `[a, b]` to `[b]`. Engine code was not weakened or distorted to satisfy an invalid oracle.

**Re-test:** 27/27 PASS.

## FR-002 — Non-finite invalid observation broke report hashing

**Observed:** expanded adversarial suite executed 37 tests and `test_nonfinite_observation_freezes` errored. The verifier correctly recognized `Infinity` as invalid, but the raw non-finite value remained inside the criterion result. Canonical SHA-256 generation then rejected it.

**Root cause:** fail-closed classification occurred before output normalization; report serialization invariants were not preserved on the invalid-observation path.

**Correction:** invalid numeric observations are normalized to `null` in criterion detail and their paths are carried explicitly in `invalid_observations`.

**Re-test:** 37/37 PASS, followed by expanded final suite PASS.

## Evidence integrity note

Earlier `tee` files were accidentally zero-byte because `unittest` writes verbose progress to stderr. Final evidence capture redirects `2>&1` before `tee`; zero-byte interim logs are excluded from the publication manifest.
