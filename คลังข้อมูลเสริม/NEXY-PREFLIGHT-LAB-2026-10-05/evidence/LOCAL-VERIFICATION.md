# Local Verification Evidence

Status: PASS (reference implementation only)
Date context: 2026-10-05
Environment: isolated ChatGPT container, Python 3.13.5

## E1 — Static compile
Command:
`python -m py_compile nexy_preflight.py cli.py`

Result: PASS.

## E2 — Unit/regression suite
Command:
`python -m unittest discover -s tests -v`

Result: PASS — 35 tests.

Covered negative paths include:
- mutation outside authorized scope;
- protected-scope mutation;
- missing irreversible-action approval;
- unknown evidence policy;
- insufficient evidence class;
- explicit failing evidence;
- duplicate claim IDs;
- orphan evidence;
- protection relaxation across task revisions;
- authority removal;
- approval removal;
- irreversible operation injection;
- write-scope expansion;
- repository-identity case handling;
- lexical dot/dot-dot normalization.

## Deterministic replay check
`python verify.py` permuted four representative canonical-JSON keys across all 24 permutations.

Observed unique hashes: `1`.

Result: PASS for this reference check.

## Acceptance vectors
The bundled `fixtures.json` corpus produced:
- `task-safe` -> PASS.
- `task-protected-write` -> CONFLICT.
- `task-evidence-gap` -> NOT_VERIFIED.

`verify.py` evaluates these vectors directly. The standalone `cli.py` accepts one task-contract object per JSON file and returns exit 0 only for PASS; non-PASS decisions return exit 2.

## Evidence boundary
These checks prove only the local reference implementation at E1/E2 and deterministic fixed-vector behavior.
They do NOT prove NEXY.AI integration, runtime operation, deployment, production security, or user acceptance.
