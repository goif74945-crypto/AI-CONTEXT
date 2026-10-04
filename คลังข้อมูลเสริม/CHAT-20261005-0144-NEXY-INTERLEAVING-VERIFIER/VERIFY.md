# Verification Record — NEXY Deterministic Interleaving Verifier

Status: PASS for isolated artifact creation and E1/E2 reference-verifier behavior.  
NEXY production integration/runtime: NOT_VERIFIED and not claimed.

Execution reference: `CHAT-20261005-0144-NEXY-INTERLEAVING-VERIFIER`  
Platform ChatGPT chat ID: UNKNOWN because the available tools do not expose it.

## Verified commands

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m interleaving_verifier fixtures/confluent.json --output /tmp/ndiv-pass.json
PYTHONPATH=src python -m interleaving_verifier fixtures/divergent.json --output /tmp/ndiv-fail.json
```

JSON Schema draft 2020-12 validation was executed with `jsonschema 4.26.0` against both schemas, both fixtures, and both captured reports.

## Results

- E1 compile/static importability: PASS.
- E2 test suite: 29/29 PASS.
- Exact oracle: all 64 three-action programs from `{add1, add2, set0, set1}` matched brute-force permutation semantics.
- Action-array permutation invariance test: PASS.
- Scale regression: 10 unordered commuting actions represent `10! = 3,628,800` complete schedules yet exact state merging explored 1,024 unique states / 5,120 transitions and returned one terminal state `{x: 10}`.
- Confluent fixture CLI: exit 0, `PASS / CONFLUENT`, 4 states, 4 transitions.
- Divergent fixture CLI: exit 2, `FAIL / DIVERGENT_TERMINAL_STATE`, 5 states, 4 transitions, witness pair `candidate-a / candidate-b`.
- Invalid input / cycle / missing dependency: fail-closed tests PASS.
- Exploration budget exhaustion: `NOT_VERIFIED / FREEZE_LIMIT` tests PASS.
- Intermediate invariant violation: decisive FAIL test PASS.
- Floating-point canonical value rejection: PASS.

## Defect found and repaired during verification

Initial negative testing found that the effect validator accepted irrelevant fields, specifically a `copy` effect carrying `value` and a `set` effect carrying `from`. Those inputs were semantically ambiguous because the engine ignored the extra fields. Two regression tests failed before repair. Validation was tightened to reject operation-inapplicable fields. Final suite after repair: 29/29 PASS.

## GitHub artifact identity

A read-back audit compared Git blob SHA for the tested local artifacts against `goif74945-crypto/AI-CONTEXT` after upload.

Result: 20/20 checked artifacts MATCH, including all runtime source, tests, fixtures, schemas, captured reports, and core design documents. See `evidence/BLOB-MANIFEST.md`.

This binds the E1/E2 claims to the exact checked GitHub blobs despite concurrent writes to the repository by other chats.

## Concurrent repository behavior observed

Several GitHub contents writes returned HTTP 409 because other chats advanced the default branch between operations. No force update, reset, rebase, or overwrite was used. Failed creates were existence-checked and retried individually against the new HEAD. No sibling lab was modified.

## Evidence files

- `evidence/final-verification.txt`
- `evidence/BLOB-MANIFEST.md`
- `evidence/confluent-report.json`
- `evidence/divergent-report.json`
- `06_TEST_MATRIX.md`

## Verification boundary

PASS proves behavior of the bounded declarative reference model only. It does not prove that a real NEXY action is atomic, that a future adapter models every externally visible intermediate state, that unbounded concurrency is safe, or that this component is deployed/integrated into NEXY.AI.
