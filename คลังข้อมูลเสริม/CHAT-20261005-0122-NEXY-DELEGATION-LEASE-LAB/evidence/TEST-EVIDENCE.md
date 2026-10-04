# TEST EVIDENCE

Workstream: `CHAT-20261005-0122-NEXY-DELEGATION-LEASE-LAB`  
Target: standalone `reference/` package only  
Date: 2026-10-05 +07

## E1 — Compile
```bash
cd reference
PYTHONPATH=src python -m compileall -q src tests examples
```
Observed: successful exit. Status: PASS for Python syntax compilation.

## E2 — First unit run
15 tests attempted; 14 passed; 1 ERROR.

Root cause: `JournalEvent` used `slots=True`, but append attempted `event.__dict__`. Slotted dataclasses have no `__dict__`.

Correction:
- use `dataclasses.replace(event, record_hash=...)`;
- remove set-derived child-effect tuple ordering to preserve deterministic input order.

The failure is retained as evidence, not erased.

## E2 — Repaired and expanded suite
Repair: 15/15 PASS.  
Expanded regression: 21/21 PASS.

Final observed:
```text
Ran 21 tests in 0.013s
OK
```

Coverage includes high-impact allow/deny, invalid index, commit-after-FREEZE rejection, destination drift, 1000 repeated deterministic evaluations, malformed fields, monotonic child delegation, and hash-chain tamper detection.

## E1 — JSON syntax
Both schema files parsed with stdlib `json.loads`. PASS for syntax only; full Draft 2020-12 meta-validation NOT_VERIFIED.

## E2/example — Demo
Exact allowed demo input returned `ALLOW` with reason `LEASE_VALID`.

## Repository byte-identity audit
After merge, GitHub `main` blob SHAs were compared against local `git hash-object`.

Exact matches observed for:
- `model.py` = `1cf018d963361f36a1528a01c2b205ecd5a234a7`
- `canonical.py` = `3dad124e335f23f5ebcc336d23c97a8688fa5640`
- `policy.py` = `61e13678a4d1ff7d076ebd3f3e0984248e43bec3`
- `journal.py` = `10f36b96388fbaafc7bfc118c7c8c80ecb03f203`
- `__init__.py` = `d13bf4e676cb56eced96851fa307f38ed2b5ff11`
- reference README = `777d70b7ff81ae44686fe23f48472035410d37ff`
- action schema = `8677a380ee4537f848fb6cd3da8ea46cbfda8357`
- lease schema = `5bb4d1047c7f5ccd5539568430c693f52c1bd6ce`
- pyproject = `a3b0193f29a9dc3cde32050e522f076346c6fd4b`

The initial committed test/demo had formatting-only byte differences. Correction blobs were created from the exact locally tested bytes:
- test suite expected blob = `4b24a593c09051202eb8392fee26f5aaf5568384`
- demo expected blob = `30f6af16f6dfb4c9228b46563c90af24f5c2ea2a`

Final repository verification must re-read these two SHAs after correction merge.

## NOT_VERIFIED
NEXY integration, concurrency atomicity, distributed revocation, signing, provider resource canonicalization, full schema conformance, deployment/performance, and user usefulness.
