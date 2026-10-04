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
Ran 21 tests
OK
```

Added coverage includes high-impact allow, invalid index, commit-after-FREEZE rejection, destination drift, 1000 repeated deterministic evaluations, malformed fields, and tamper detection.

## E1 — JSON syntax
Both schema files parsed with stdlib `json.loads`. PASS for syntax only; full Draft 2020-12 meta-validation NOT_VERIFIED.

## E2/example — Demo
Observed ALLOW with reason `LEASE_VALID` for exact demo input and bound plan hash. PASS for that example.

## NOT_VERIFIED
NEXY integration, concurrent atomicity, distributed revocation, cryptographic signing, provider resource canonicalization, full JSON Schema conformance, deployment/performance, and user usefulness hypothesis.
