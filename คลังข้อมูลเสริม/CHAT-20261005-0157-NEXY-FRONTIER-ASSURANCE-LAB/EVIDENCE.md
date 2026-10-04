# Verification Evidence

## Local runtime
- Date: 2026-10-05 Asia/Bangkok
- Python: 3.13.5
- Environment: isolated local sandbox
- External dependencies: none

## Failure → Fix → Retest
Initial extended verification:
- 26 tests: PASS
- benchmark: FAIL with `ModuleNotFoundError: frontier_lab`
Root cause: benchmark executed from `benchmarks/`, so package root was absent from sys.path.
Correction: add repository-root path from `Path(__file__).resolve().parents[1]`.
Fresh rerun after correction:
- compile: PASS
- 26 tests: PASS
- benchmark: PASS

## Canonical bundle fresh proof
Commands:
`python3 -m compileall -q frontier_assurance_lab.py test_frontier_assurance_lab.py`
`python3 -m unittest -v test_frontier_assurance_lab.py`

Observed:
- Ran 26 tests
- failures: 0
- errors: 0
- result: OK

Coverage includes:
- positive behavior;
- negative/freeze behavior;
- integration across all five systems;
- 100 input-order permutations each for MUSCLE, PAREX, GHOSTEDGE.

## Exact tested content hashes
- frontier_assurance_lab.py SHA-256: `44d01377712c7eb6da7a635725bb2c0e0997d54a7c5ad0f18c5fab440770551c`
- test_frontier_assurance_lab.py SHA-256: `caab77819f970433ca3686b9008bec834040a4e072a8f744389a7a45de6f8030`

## Synthetic smoke benchmark
Measured on the sandbox only; not a production latency guarantee.
- MUSCLE exact 12-constraint core: 12.340 ms; core size 12
- PAREX 500 plans: 52.990 ms; frontier size 76
- GHOSTEDGE 5,000 experiments: 4.651 ms; candidates 1
- RECERT 5,000 state leaves: 11.518 ms; CERTIFIED
- OBSURE 500 effects / 2,000 event specs: 1.518 ms; PASS

## Evidence classes
- E1: compile/static import execution PASS
- E2: 26 unit/adversarial tests PASS
- E3: pipeline integration tests PASS
- E5/E6: NOT PERFORMED; these are standalone research components, not deployed NEXY runtime


## Repository persistence verification
Read-back performed from `main` after persistence repair.

- Persisted implementation Git blob: `db607b90ef2fc0227d754bfabcddbee050b32f29`
- Local exact-tested implementation Git blob: `db607b90ef2fc0227d754bfabcddbee050b32f29`
- Persisted test Git blob: `8c9a588fa579acde4ecb918d43e8cb4c0d8459b0`
- Local exact-tested test Git blob: `8c9a588fa579acde4ecb918d43e8cb4c0d8459b0`
- Test persistence correction commit: `2b6b9987f72177373c2b877aa48f2e72dd960614`
- Binding verdict: **PASS — exact tested bytes are the persisted bytes for implementation and tests.**

Fresh post-binding local verification:
- compileall: PASS
- unittest: **26/26 PASS**, 0 failures, 0 errors
- implementation SHA-256: `44d01377712c7eb6da7a635725bb2c0e0997d54a7c5ad0f18c5fab440770551c`
- test SHA-256: `caab77819f970433ca3686b9008bec834040a4e072a8f744389a7a45de6f8030`

### Integrity incident preserved
The first persisted test artifact did not match the tested local blob. This was detected by read-back, not ignored. The persisted test was corrected twice: first to restore missing imports, then to restore the exact trailing newline required for byte identity. Final Git blob matches the local tested artifact exactly.
