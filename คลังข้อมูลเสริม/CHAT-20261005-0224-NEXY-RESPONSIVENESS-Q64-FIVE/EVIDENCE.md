# Evidence Record

## Evidence correction
The earlier 34-test count belongs to the larger local pre-write suite. The first durable serialization stored a compact 22-method suite. Exact PASS claims below are bound to the durable bytes actually stored.

## Exact durable target
- repository: `goif74945-crypto/AI-CONTEXT`
- code/test introduction commit: `80cf0db8b300312b39347c5eff286a64b7365854`
- work folder: `คลังข้อมูลเสริม/CHAT-20261005-0224-NEXY-RESPONSIVENESS-Q64-FIVE`
- Python files verified: 15 (7 source + 8 tests)

## Byte identity proof
All 15 source/test files were fetched with GitHub `fetch_file` at the exact commit. Returned Git blob SHA values were compared against local `git hash-object` values for reconstructed files. Result: 15/15 exact matches.

## E1
- `PYTHONPATH=src python -m compileall -q src tests`: PASS, exit 0.
- AST float scan across `src/**/*.py` + `tests/**/*.py`: PASS, 0 float literals.

## E2
- `PYTHONPATH=src python -m unittest discover -s tests -v`
- observed exact durable result: `Ran 22 tests in 0.103s`, `OK`, exit 0.
- seeded invariant iterations: Q64 500 + latency 200 + prefetch 200 + proof DAG 100 + warmset 200 + attention 200 = 1,400.

## E3
Durable `tests/test_integration.py` executes all five modules in one isolated pipeline and passed.

## Limits
No exact NEXY.AI implementation integration, browser/E2E, production benchmark, deployment proof or Canon promotion was performed.
