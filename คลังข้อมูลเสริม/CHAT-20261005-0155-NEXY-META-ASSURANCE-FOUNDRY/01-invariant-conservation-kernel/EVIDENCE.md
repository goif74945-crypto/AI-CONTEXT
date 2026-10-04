# Evidence — Invariant Conservation Kernel (ICK)

Truth class: `REFERENCE_IMPLEMENTATION_EVIDENCE`, not NEXY production proof.

## Claims proved locally
- E1: `src/ick.py` compiles under Python 3.13.5.
- E2: 10 unit/negative tests pass.
- E2 differential/exhaustive: 65,536 transition combinations were compared against an independently written conservation predicate in `deep_validation.py`; no mismatch was observed.
- E3-local: the root integration smoke imports ICK from its file boundary and executes a representative legal transition.

## Negative paths covered
- authority inflation without grant;
- evidence inflation without references;
- uncertainty erasure without resolution;
- constraint weakening without waiver;
- capability escalation without grant;
- side effect outside declared capability;
- legal typed exceptions;
- deterministic fingerprint behavior.

## Exact local commands
```text
python3 -m compileall -q .
python3 -m unittest discover -s 01-invariant-conservation-kernel/tests -p 'test_*.py'
python3 integration_smoke.py
python3 deep_validation.py
```

## Limitations
- Receipt authenticity/authorization is not cryptographically or policy verified by ICK v1.
- Authority/evidence levels are abstract integers supplied by the integrating boundary.
- No live NEXY integration, runtime, deployment or user-impact claim is made.
