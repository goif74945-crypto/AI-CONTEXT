# Validation Report

Status at local verification checkpoint: **PASS for the reference implementation's stated E1/E2 claims**.

## Environment
- Isolated container sandbox.
- Python standard library only.
- No network required for test execution.
- No NEXY.AI repository mutation.

## E1 — Static compilation
Command:

```text
python -m py_compile reference_impl/trustux.py tests/test_trustux.py
```

Observed: process exit success, no compiler output.

Status: **PASS**.

## E2 — Unit behavior
Command:

```text
python -m unittest discover -s tests -p 'test_*.py' -v
```

Observed: **20 tests run, 20 passed, 0 failed, 0 errors**.

Covered claims include:
- STABLE + supplied release proof -> RESULT;
- STABLE without integrity hash -> HOLD;
- releaseable=false -> HOLD;
- FREEZE always visible and result hidden;
- OWNER Recover only when recoverable=true;
- OPERATOR receives no Recover action;
- STOP exposes no Recover action;
- VERIFYING is PENDING, not success;
- READY action visibility varies by role;
- DEGRADED status is exposed;
- unknown incident code is preserved without guessed interpretation;
- invalid state fails closed;
- missing trace identity fails closed;
- invalid freeze metadata fails closed;
- same input + role yields identical output/fingerprint;
- role changes visible action contract without changing authoritative system state;
- stale output payload remains hidden during FREEZE;
- PUBLIC_USER does not receive a mutation action on READY.

## E1 — JSON parse check
Schema and fixture JSON files are parsed during final local audit. JSON parse success proves syntactic validity only, not full JSON-Schema conformance.

## Not proven
- E3 integration with real NEXY backend/frontend.
- E4 browser/user-flow behavior.
- Accessibility conformance.
- Localization behavior.
- Deployment/runtime behavior.
- Canonical adoption into NEXY.

Those remain **NOT_VERIFIED** by design.
