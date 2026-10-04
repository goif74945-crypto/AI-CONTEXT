# HCAS Verification Evidence

Date: 2026-10-05
Environment: ChatGPT execution container, Python 3.11+ virtual environment
Scope: local project artifact prior to GitHub write-back

## E1 — Static compile
Command:
`python scripts/run_checks.py`

Observed:
`E1 compile: PASS`

Status: **PASS** for Python syntax/bytecode compilation of `src/**/*.py`.

## E2 — Unit behavior
Command:
`python -m unittest discover -s tests -v`

Observed:
- 11 tests executed
- 11 passed
- 0 failed
- runtime approximately 0.002s in observed container run

Covered negative paths include:
- UI visibility without backend authorization;
- loading state incorrectly treated as evidence;
- maskable FREEZE;
- duplicate action identity;
- missing rollback path;
- missing irreversible warning;
- strict-future destructive action without dual approval;
- deterministic identical-output check;
- non-object manifest failure.

Status: **PASS** (E2).

## CLI contract proof
Observed commands used `PYTHONPATH=src python -m hcas.cli ...`.

Results:
- `examples/safe_manifest.json` -> exit `0`, report `PASS`, 0 errors.
- `examples/unsafe_manifest.json` -> exit `2`, report `FAIL`, 14 errors + 2 warnings.
- malformed JSON -> exit `64`, report `INVALID_INPUT` on stderr.

Status: **PASS** for the declared CLI exit contract.

## Limitations
- This is not E3/E4 proof of a NEXY backend/UI.
- JSON Schema was authored but not validated by an external JSON-Schema engine because the implementation intentionally has zero runtime dependencies.
- No NEXY.AI repository was modified or executed.
