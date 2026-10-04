# Local Verification Evidence

Status: PASS (reference implementation only)
Date context: 2026-10-05
Environment: isolated ChatGPT container, Python 3.13.5

## E1 — Static compile
Command:
`python -m compileall -q src/nexy_preflight`

Result: PASS.

## E2 — Unit/regression suite
Command:
`PYTHONPATH=src python -m unittest discover -s tests -v`

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
`scripts/verify_reference.py` permuted four representative canonical-JSON keys across all 24 permutations.

Observed unique hashes: `1`.

Result: PASS for this reference check.

## Acceptance vectors
- `task-safe.json` -> PASS, exit 0.
- `task-protected-write.json` -> CONFLICT, exit 2.
- `task-evidence-gap.json` -> NOT_VERIFIED, exit 2.

## Evidence boundary
These checks prove only the local reference implementation at E1/E2 and deterministic fixed-vector behavior.
They do NOT prove NEXY.AI integration, runtime operation, deployment, production security, or user acceptance.
