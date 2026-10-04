# Evidence & Limitations

## Executed local evidence
Environment: Python 3.13.5, no third-party runtime dependencies.

### TDD history
- Initial RED: tests existed before implementation; import failed because `epistemic_integrity.py` did not exist.
- First GREEN: 15/15 PASS.
- Adversarial RED: expanded suite exposed two DMAG gaps: duplicate observation IDs and non-finite numeric dimension values.
- FIX: added unique-ID and finite-number validation.
- Integration-gate RED: gate import failed before implementation.
- Fixture audit later found a test-rule modeled as “live” was actually redundant because its effect equaled default policy behavior; the fixture was corrected instead of weakening production semantics.

### Final fresh gates
- `python -m compileall -q epistemic_integrity.py tests` → exit 0.
- `PYTHONHASHSEED=1 python -m unittest discover -s tests -v` → 37 tests, OK.
- `PYTHONHASHSEED=777 python -m unittest discover -s tests -v` → 37 tests, OK.
- `python run_all_tests.py` → compile gate + 37 tests, OK.
- Five seeded order-invariance tests execute 500 total permutation/insertion iterations.
- Core AST import scan: only `__future__`, `dataclasses`, `itertools`, `math`, `typing`; no socket/requests/urllib/subprocess/pathlib/os/random/time/datetime imports; no dynamic exec/eval/compile calls.
- Targeted common token/private-key pattern scan → 0 findings.

## Evidence classes
Local E1 syntax/static and E2 unit/adversarial/property/integration-composition only. No E3 NEXY integration, E4 E2E, E5 runtime/operations, E6 deployment or E7 physical claim.

## Limitations
- ECOF validates claim graph grounding, not truth of external evidence.
- DMAG audits one numeric dimension per invocation and trusts the authoritative verdict order supplied by caller.
- PDZA v0.1 uses equality conditions and exact finite domains; it intentionally freezes on combinatorial overflow.
- RKM is in-memory and trusts explicit premise/authority identity inputs; no durable distributed revocation system.
- ACE has four premise classes and trusts caller classification.
- No NEXY.AI repository was modified or runtime exercised.
- Objective superiority over all prior research is NOT_VERIFIED; novelty/orthogonality is the evidenced claim.
