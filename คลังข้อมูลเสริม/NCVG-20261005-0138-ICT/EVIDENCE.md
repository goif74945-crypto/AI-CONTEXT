# NCVG Verification Evidence

## Boundary
These results prove local NCVG companion behavior only. They do **not** prove NEXY.AI runtime/deployment integration.

## Environment
- Date: 2026-10-05 (+07:00)
- Python: 3.13.5
- Runtime dependencies: Python standard library only

## E1 Static
```bash
python -m compileall -q nexy_gate tests
python -m json.tool schema/ncvg-bundle-v1.schema.json
```
Observed: PASS.

## E2 Unit/CLI
```bash
python -m unittest discover -v
```
Observed: 21 tests, OK.

Coverage includes 500 deterministic random JSON robustness cases and explicit negative paths for missing evidence, wrong evidence class, stale commit, duplicate IDs, protected/forbidden mutation, non-PASS execution status, malformed JSON, and warning policy.

## E3 Local packaging integration
```bash
python -m pip wheel . --no-deps --no-build-isolation
python -m venv <clean-venv>
<clean-venv>/bin/pip install --no-index --no-deps <built-wheel>
<clean-venv>/bin/ncvg validate examples/pass_bundle.json
<clean-venv>/bin/ncvg validate examples/freeze_bundle.json
```
Observed:
- wheel build exit 0
- clean-venv install PASS
- installed valid example ALLOW exit 0
- installed invalid/protected example FREEZE exit 2

Valid bundle SHA-256:
`96da9e9d077a7c62c35e3495cf041789875ebededde81fc2f2a4a76c7df63989`

Freeze bundle SHA-256:
`25acfaf590631674f67fcd664afe07340f49042ae82119e29c3c235d78686d7f`

Freeze codes:
- EVIDENCE_CLASS_NOT_ACCEPTED
- FORBIDDEN_REPOSITORY_MUTATION
- PROTECTED_TARGET_MUTATION

## Failure → fix evidence
Initial `python -m unittest discover -v` found 0 tests. Adding `tests/__init__.py` fixed discovery; rerun executed the full suite. Later malformed-input fuzzing exposed a type robustness edge, which was hardened to fail closed and re-tested.

## Limitations
- NEXY.AI adapter integration: NOT_VERIFIED
- independent audit provenance: NOT_IMPLEMENTED
- cryptographic authenticity: NOT_IMPLEMENTED
- deployment evidence: NOT_VERIFIED
- production authorization: NOT_VERIFIED
