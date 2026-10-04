# Verification Evidence

Status before GitHub upload: `PASS` for local implementation evidence, pending repository readback.

## Evidence classes
- E1 static: `python -m compileall -q src tests` => exit 0.
- E2 unit/regression: `PYTHONPATH=src python -W error -m unittest discover -s tests -v` => all tests PASS.
- Local integration: real CLI subprocess generated sealed snapshots and enforced strict/permissive policy outcomes.

## TDD / failure-repair evidence
- `RED-TEST.txt`: implementation absent; import failure observed before production code.
- `RED-ADVERSARIAL.txt`: invalid UTF-8 and resealed semantic/schema tampering exposed four failures.
- `GREEN-ADVERSARIAL.txt`: all four repaired cases pass.
- `RED-SECURITY-LIMITS.txt`: credential-bearing source and missing input-size gate exposed failures.
- `GREEN-SECURITY-LIMITS.txt`: both repaired cases pass.
- `RED-CROSS-ORIGIN.txt`: version change masked registry-origin change.
- `GREEN-CROSS-ORIGIN.txt`: origin change independently classified and policy-enforced.

## Final local regression
See `FINAL-UNIT-TEST.txt` and `GREEN-REGRESSION-3.txt`.

## CLI integration
See `CLI-INTEGRATION.txt`:
- strict version drift => exit 2 + `FREEZE` + `DRIFT_VERSION_CHANGE_DENIED`.
- explicitly version-permissive policy => `ALLOW` for same-origin version change.
- hashed Python requirement => `ALLOW` sealed snapshot.

## Performance smoke
See `PERFORMANCE-SMOKE.txt`. This is informational only and is not a deployment/runtime guarantee.

## Limitations
- No live registry lookup, vulnerability scan, signature verification, SLSA/Sigstore verification, or reproducible build execution in v0.1.
- SHA-256 snapshot seals provide integrity consistency, not signer identity/authenticity.
- npm support is lockfileVersion 2/3 package maps only.
- Python requirements support is intentionally strict exact-pin syntax; complex pip grammar freezes.
- No claim is made that this code is integrated into NEXY.AI; it is a standalone compatible reference implementation.
