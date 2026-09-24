# Executable Closed-Loop Runtime Validation

## Result
**PASS — local executable core / NOT_VERIFIED external worker transport**

## Executed evidence
Command executed locally:

`python3 -m unittest -v test_loop_engine.py`

Result:

- tests run: **12**
- failures: **0**
- errors: **0**

Validated behavior:
- deterministic priority/sequence scheduling;
- exact-HEAD stale rejection;
- path collision exclusion;
- resource collision exclusion;
- worker scope/capacity gating;
- human gate fail-closed + explicit approval;
- lease expiry handling;
- heartbeat epoch/sequence checks;
- dependency-cycle rejection;
- bounded deterministic retry delay;
- Builder PASS requires evidence and re-audit;
- Auditor PASS is required before COMPLETED;
- convergence remains fail-closed.

## Additional validation
- `loop_engine.py` compiled with `python3 -m py_compile`: PASS.
- `runtime-envelope.schema.json` parsed and validated against golden example with Python `jsonschema`: PASS.
- filesystem spool smoke test imported HEAD + worker + command, acquired claim, and emitted `outbox/builder-1/command-CMD-DEMO-001.json`: PASS.

## Evidence boundary
This proves the runtime core logic executed locally in an isolated test environment.
It does **not** prove:
- a real ChatGPT/Work worker adapter;
- NEXY implementation mutation;
- distributed multi-host locking;
- production/deployment execution;
- 24/7 soak stability.

Those require separate adapter/integration/soak evidence.
