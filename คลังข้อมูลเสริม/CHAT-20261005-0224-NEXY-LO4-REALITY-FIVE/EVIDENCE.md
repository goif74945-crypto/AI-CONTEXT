# Evidence Record

Execution: `CHAT-20261005-0224-NEXY-LO4-REALITY-FIVE`

## Evidence classes

### E1 static
- `lo4_reality_five.py` compiled successfully.
- `test_lo4_reality_five.py` compiled successfully.

### E2 unit/integration
Final suite: **28 tests PASS**.
Coverage includes:
- Q64.64 construction/arithmetic/overflow/division-by-zero;
- OAC mandatory visibility, deterministic tie, duplicate rejection;
- JCPP hard-filter precedence, freeze when no legal route, deterministic tie;
- SAEM pass/fail for required atoms and digest mutation;
- HIG auto/ask/approval/freeze precedence;
- VIBA mandatory-budget freeze, exact frontier behavior, tie cost, monotonic contract, fixed tie regression;
- integrated pipeline waiting-human and freeze cases;
- integrated order determinism.

Raw output: `evidence/verify-output.txt`.

### E2 stress / deterministic behavior
`stress_verify.py` executed:
- OAC: 20,000 notices;
- JCPP: 10,000 candidate placements;
- SAEM: 50,000 semantic atoms;
- VIBA: 40 obligations × 6 enhancement tiers;
- reverse-order digest equivalence for OAC/JCPP/SAEM/VIBA.

All checks passed. Raw JSON: `evidence/stress-output.json`.

### Hash-seed regression
Unit suite passed with `PYTHONHASHSEED=1,2,99,123456`. Raw outputs are stored under `evidence/`.

## Defect / fix evidence
Stress verification initially failed in VIBA with a `TypeError` caused by tuple tie-breaking across `None` and string tier IDs. The defect was corrected by canonicalizing choices to `(obligation_id, tier_id_or_empty_string)` before comparison. A dedicated regression test was added. The final stress run passed.

## Local performance observations
The stress-output file includes elapsed times from one Python 3.13.5 runtime. These are environment observations only and **must not be treated as production SLOs**.

## NOT VERIFIED
- integration with the NEXY.AI implementation repository;
- production deployment;
- real provider metadata correctness or legal compliance;
- accessibility standards conformance;
- production workload performance;
- security review against hostile external inputs;
- UX/user-study evidence;
- Canon promotion.

## Modularization re-verification
- Compiled Python files: 20
- Unit/integration tests after modularization: 28 PASS
- Stress suite after modularization: PASS with unchanged deterministic digests
- Hash-seed checks: `1`, `2`, `99`, `123456` PASS
- This refactor was performed only to make publication through the connected GitHub text API safe and reviewable; behavior remained invariant under the existing tests and stress digests.
