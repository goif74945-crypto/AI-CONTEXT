# HCAS Verification Evidence

Date: 2026-10-05
Environment: ChatGPT execution container, Python 3.11+ virtual environment
Repository target: `goif74945-crypto/AI-CONTEXT`
Project path: `คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-HUMAN-CONTROL-ASSURANCE`

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
- runtime approximately 0.002s in the observed container run.

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

## E0 — Repository presence and tested-content identity
GitHub write path used a dedicated branch and PR because concurrent sessions repeatedly advanced `main`; no force update was used.

Observed:
- PR #5 merged successfully.
- merge commit: `83c46e1e03e03151a2db0541130042fd38060a59`.
- repository project directory re-read from `main`: PASS.
- `src/hcas/validator.py` on `main`: blob SHA `3ccc9ac1a95c14ae72ceaa34b5ad6248e84d63ad`.
- `tests/test_validator.py` on `main`: blob SHA `df60f788048168a15573393419fdbbffb70d49c9`.
- those SHAs match the blobs created from the locally tested contents.

Status: **PASS** for repository presence and content identity.

## Scope evidence
The pre-merge compare reported 22 changed files and **0 paths outside**
`คลังข้อมูลเสริม/CHAT-20261005-0122-NEXY-HUMAN-CONTROL-ASSURANCE/`.

Two earlier direct fast-forward attempts were rejected by GitHub with `Update is not a fast forward` while other sessions advanced `main`; no force push was used.

## Limitations
- This is not E3/E4 proof of a NEXY backend/UI.
- JSON Schema was authored but not validated by an external JSON-Schema engine because the implementation intentionally has zero runtime dependencies.
- No repository whose name contains `NEXY.AI` was modified or executed by this HCAS workflow.
