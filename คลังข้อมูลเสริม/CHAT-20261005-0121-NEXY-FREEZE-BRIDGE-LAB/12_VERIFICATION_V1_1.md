# v1.1 Verification Report

Classification: **EXECUTED LOCAL EVIDENCE FOR THE REFERENCE IMPLEMENTATION ONLY**

## Scope of proof

This report proves properties of the isolated Freeze Bridge v1.1 reference implementation in the execution sandbox. It does not prove current NEXY integration, browser UX, runtime operations, deployment, or release readiness.

## Unit + negative-path tests

Command shape:

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
```

Observed:
- 23 tests
- 23 passed
- 0 failures
- 0 errors

Covered behavior includes:
- deterministic normalization;
- upstream-intent intersection;
- missing-input sorting;
- unknown string reason → UNKNOWN_REASON;
- malformed non-string reason rejection;
- restricted security evidence suppression;
- restricted non-security public-reference filtering;
- dependency-recheck safety clamp;
- localization semantic invariance;
- no missing-input leakage for unrelated reasons;
- control-character rejection;
- invalid intent rejection;
- protocol-version rejection;
- context label non-reflection;
- enum/list/bounds validation;
- CLI success/failure paths;
- explicit sibling boundary excluding role/display mode/UI actions.

## Coverage

Executed with branch coverage.

Production library:
- `freeze_bridge/__init__.py`: 100%
- `freeze_bridge/compiler.py`: 100%
- `freeze_bridge/model.py`: 100%
- `freeze_bridge/policy.py`: 100%

Production library line + branch coverage: **100% in this run**.

The combined report including the test module is 99% because the discovery runner does not execute the test file's `unittest.main()` line.

## Syntax/static execution

```bash
python -m compileall -q freeze_bridge tests tools
```

Observed: PASS.

## Policy matrix

`tools/policy_selfcheck.py` enumerates:
- 11 reasons
- 2 locales
- 3 disclosure classes
- 5 statuses

Total: 330 cases.

Observed:
`PASS policy_matrix_cases=330`

Each case checks:
- repeat determinism;
- eligible intents remain within reason policy;
- downstream UI authority remains required;
- no Trust UX role/display/action keys leak into output;
- restricted security does not expose evidence;
- security/unknown do not become dependency-recheck safe.

## JSON Schema verification

Schemas:
- `schema/freeze-event.schema.json`
- `schema/freeze-explanation.schema.json`

Draft 2020-12 schema self-check: PASS.

Input→compiler→output schema round-trip:
- `examples/missing-input.th.json`: PASS
- `fixtures/security-restricted.json`: PASS
- `fixtures/unknown-reason.json`: PASS

## CLI JSON proof

Thai example compiled through `python -m freeze_bridge ... --compact` and parsed through `python -m json.tool`.

Observed: PASS.

## Microbenchmark

Final measured sample in the execution sandbox:

- iterations: 50,000
- elapsed: 1.516704 seconds
- rate: 32,966.23 compiles/second
- stable sample fingerprint generated

This is environment-specific microbenchmark evidence only, **not** an E5 load claim or production SLA.

## Evidence classification

- E0 local artifact presence: PASS
- E1 syntax/schema/coverage instrumentation: PASS
- E2 isolated behavior: PASS
- E3 NEXY integration: NOT_VERIFIED
- E4 real UI/user flow: NOT_VERIFIED
- E5 target runtime/operations: NOT_VERIFIED
- E6 deployment: NOT_VERIFIED

## Historical test defect

Before v1.1, the initial v1.0 suite had one false failure because a test searched substring `script` and matched JSON key `description`. The assertion was corrected to test actual payload markers. This history is retained because hiding test defects would make the evidence record worse, not prettier.


## Clarification: localization evidence

The Thai/English test in this suite proves that locale selection does not change machine-semantic output fields. It does **not** prove that the English and Thai prose are linguistically equivalent.

A concurrent sibling, `NEXY Semantic Localization Integrity Lab`, owns deterministic high-risk localization-drift checks. Full localization correctness remains NOT_VERIFIED here.
