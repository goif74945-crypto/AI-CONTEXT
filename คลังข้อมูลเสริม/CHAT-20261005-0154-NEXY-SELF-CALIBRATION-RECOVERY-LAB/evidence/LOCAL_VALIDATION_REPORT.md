# Local Validation Report

Status: PASS for the local reference implementation claims enumerated below. This is not NEXY production/integration/deployment proof.

## Environment
- Python: 3.13.5
- Platform: Linux-6.18.44-x86_64-with-glibc2.41

## Executed gates
- E1 static syntax/import gate: `python -m compileall -q .` → exit 0.
- E2/E3-local suite: `python -m unittest discover -s . -p 'test_*.py' -v` → 38/38 PASS.
- Integration demo: `python demo.py` → exit 0; output SHA-256 `894972ebe792614603aa174c43e6534605d6768d0751160b41eeafad317ba8b4`.
- Performance smoke: `python -m integration.benchmark_smoke` → exit 0; local observation only.

## Test distribution
- Contract Archaeologist: 8 focused tests.
- Failure Atomizer: 7 focused tests.
- Calibration Observatory: 6 focused tests.
- PauseSafe Kernel: 6 focused tests.
- Evidence Genealogy Engine: 5 focused tests.
- Cross-concept adversarial matrix: 5 tests.
- Portfolio integration: 1 test.
- Total: 38.

## Adversarial coverage highlights
- 24 permutations of the same four trace events produce identical Contract Archaeologist output.
- All 28 two-element trigger pairs from an 8-item universe reduce to the correct 1-minimal witness.
- Evidence correlation is transitively closed across source/content links.
- PauseSafe state matrix covers every status × idempotent × checkpointed × compensated combination.
- Balanced low/high confidence population verifies zero aggregate calibration error in the constructed case.

## Local performance smoke (median)
These are environment-specific observations, not budgets or SLAs:
- Contract Archaeologist, 2,000 events: 0.01320 s.
- Evidence Genealogy, 20,000 items: 0.04116 s.
- Calibration Observatory, 100,000 records: 0.04035 s.
- PauseSafe, 50,000 steps: 0.00304 s.
- Failure Atomizer, 2,048 items: 0.00174 s, 158 predicate evaluations, minimal witness size 2.

## Limitations
- No production NEXY adapter exists in this mission.
- No E4/E5/E6 production runtime/deployment evidence.
- Benchmark variance exists and no production resource envelope was measured.
- Novelty review was constrained by unavailable GitHub code-search indexing; selected near-neighbor specs and top-level inventory were inspected instead.
