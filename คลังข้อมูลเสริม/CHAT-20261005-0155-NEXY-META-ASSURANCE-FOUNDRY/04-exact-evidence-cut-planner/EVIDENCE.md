# Evidence — Exact Evidence Cut Planner (EECP)

Truth class: `REFERENCE_IMPLEMENTATION_EVIDENCE`, not NEXY production proof.

## Claims proved locally
- E1: `src/eecp.py` compiles under Python 3.13.5.
- E2: 12 unit/negative tests pass.
- E2 differential/exact: 120 generated AND/OR formula families over four evidence leaves were compared with independent brute-force truth enumeration and independent hitting-set enumeration. Proof frontiers and minimal cutsets matched.
- E3-local: root integration smoke imports EECP and executes a representative acquisition plan.

## Negative / boundary paths covered
- cycles;
- missing child nodes;
- duplicate IDs;
- invalid costs/operators;
- invalid proven evidence IDs;
- proof-frontier bound exhaustion;
- cutset-enumeration bound exhaustion;
- deterministic cost/tie ordering.

## Exact local commands
```text
python3 -m compileall -q .
python3 -m unittest discover -s 04-exact-evidence-cut-planner/tests -p 'test_*.py'
python3 integration_smoke.py
python3 deep_validation.py
```

## Limitations
- Exact enumeration is intentionally bounded and can become exponential; bound exhaustion fails closed rather than approximating a proof.
- Evidence costs are advisory positive integers supplied by the integrating system.
- A graph route proves only the declared graph semantics; it does not establish that evidence artifacts are truthful.
- No live NEXY proof graph integration is claimed.
