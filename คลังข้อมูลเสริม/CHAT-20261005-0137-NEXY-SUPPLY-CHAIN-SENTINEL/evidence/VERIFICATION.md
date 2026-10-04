# Verification Evidence

Status: `PASS` for the reference implementation evidence described below. This does not claim NEXY.AI integration, deployment, registry authenticity, or vulnerability safety.

## Evidence classes
- E1 static: `python -m compileall -q src tests` => exit 0.
- E2 unit/regression: `PYTHONPATH=src python -W error -m unittest discover -s tests -v` => 19/19 tests PASS.
- Local integration: real CLI subprocess generated sealed snapshots and enforced strict/permissive policy outcomes.
- E0 repository readback: exact tested code/evidence bundle committed and read back from AI-CONTEXT; see `GITHUB-READBACK.md`.

## TDD / failure-repair evidence
- `RED-TEST.txt`: implementation absent; import failure observed before production code.
- `RED-ADVERSARIAL.txt`: invalid UTF-8 and resealed semantic/schema tampering exposed four failures before repair.
- `RED-SECURITY-LIMITS.txt`: credential-bearing source and missing input-size gate exposed failures before repair.
- `RED-CROSS-ORIGIN.txt`: version change masked registry-origin change before repair.
- `FINAL-UNIT-TEST.txt`: all repaired cases plus the full regression suite pass together.

## Final local regression
See `FINAL-UNIT-TEST.txt`: 19 tests executed, 19 passed, warnings promoted to errors.

## CLI integration
See `CLI-INTEGRATION.txt`:
- strict version drift => exit 2 + `FREEZE` + `DRIFT_VERSION_CHANGE_DENIED`.
- explicitly version-permissive policy => `ALLOW` for same-origin version change.
- hashed Python requirement => `ALLOW` sealed snapshot.

## Performance smoke
See `PERFORMANCE-SMOKE.txt`. This is informational only and is not a deployment/runtime guarantee or SLA.

## Limitations
- No live registry lookup, vulnerability scan, signature verification, SLSA/Sigstore verification, or reproducible build execution in v0.1.
- SHA-256 snapshot seals provide integrity consistency, not signer identity/authenticity.
- npm support is lockfileVersion 2/3 package maps only.
- Python requirements support is intentionally strict exact-pin syntax; complex pip grammar freezes.
- No claim is made that this code is integrated into NEXY.AI; it is a standalone compatible reference implementation.
