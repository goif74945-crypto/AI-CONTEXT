# Verification Evidence

## Status

`PASS` for the standalone PCF lab at E1/E2 evidence classes described below.

This does **not** prove NEXY production integration, external-provider behavior, deployment, or legal compliance.

## Environment

- Verification date: 2026-10-05 (Asia/Bangkok task context)
- Python: 3.13.5
- Package declared minimum: Python >= 3.11
- Runtime dependencies: none

## TDD history

The implementation was created through observed RED/GREEN cycles:

1. Initial tests failed because `nexy_pcf.compiler` did not exist.
2. Initial implementation produced a GREEN suite.
3. New hardening tests exposed receipt-key, malformed policy/profile, and field-order determinism gaps; those tests failed before repair.
4. Semantic-equivalence tests exposed ALLOW/FREEZE receipt instability under list/field reordering; both tests failed before repair.
5. Malformed JSON-compatible classification/boundary tests exposed four uncaught `TypeError` paths; all four failed before repair.
6. Repairs were followed by the final fresh verification suite below.

This preserves the important distinction between a test that happens to pass and a regression test that proved a missing behavior first.

## Final built-in verifier

Command:

```bash
PYTHONPATH=src python scripts/verify.py
```

Observed:
- source compile: PASS
- JSON fixtures/schemas parsed: 8
- ALLOW fixture: PASS
- FREEZE fixture: PASS
- denied secret canary leak check: PASS
- unit/CLI tests: **32/32 PASS**
- exit code: `0`

## Deterministic malformed-input fuzzing

Command:

```bash
PYTHONPATH=src python scripts/fuzz_verify.py
```

Observed:
- seed: `20261005`
- cases: `3000`
- failures: `0`
- exit code: `0`

The harness mutates envelope, destination profile, policy, and field values using JSON-compatible malformed shapes, then requires:
- no unexpected exception;
- decision remains `ALLOW` or `FREEZE`;
- every `FREEZE` has `payload == null`;
- result remains JSON serializable.

## Independent JSON Schema validation

Using `jsonschema` Draft 2020-12 validator available in the execution environment:
- policy fixture against policy schema: PASS
- provider fixture against destination profile schema: PASS
- ALLOW envelope fixture against context schema: PASS
- FREEZE envelope fixture against context schema: PASS
- generated ALLOW result against result schema: PASS
- generated FREEZE result against result schema: PASS

This validator is verification tooling only; it is not a runtime dependency of PCF.

## Packaging verification

Command class:

```bash
python -m pip wheel --no-build-isolation --no-deps -w <temp> .
python -m pip install --no-deps --target <temp> <wheel>
```

Observed:
- wheel build: PASS
- wheel install: PASS
- installed-wheel CLI decision: `ALLOW`
- installed-wheel payload keys: `prompt`, `source_code`
- receipt algorithm: `HMAC-SHA256`
- wheel SHA-256 for this verification build: `833efe9bd21ab85b5065896e86e3ada48c561365bc50dd2dba23f482e55d8239`

Wheel bytes are not stored in AI-CONTEXT; the hash is reproducibility evidence for the local verification build only.

## Direct CLI verification

ALLOW fixture:
- decision: `ALLOW`
- payload keys: `prompt`, `source_code`
- exit: `0`

FREEZE fixture containing synthetic secret canary:
- decision: `FREEZE`
- violations: `DESTINATION_CLASSIFICATION_LIMIT`, `EXTERNAL_CLASSIFICATION_DENIED`
- secret literal present in serialized result: `false`
- exit: `2`

## Diagnostic benchmark

No production SLO is claimed. Five local runs per size produced:

| Candidate fields | Median | Min | Max | Decision |
|---:|---:|---:|---:|---|
| 100 | 1.018 ms | 0.867 ms | 1.320 ms | ALLOW |
| 1,000 | 9.227 ms | 8.866 ms | 11.557 ms | ALLOW |
| 10,000 | 112.674 ms | 102.413 ms | 141.881 ms | ALLOW |

These numbers are environment-specific diagnostics, not capacity guarantees.

## Evidence class verdict

- E0 file presence: pending until GitHub read-back seal, then recorded in completion certificate.
- E1 static/package/schema: PASS.
- E2 isolated behavior: PASS.
- E3+ integration/runtime/deployment: NOT_VERIFIED and intentionally out of scope.
