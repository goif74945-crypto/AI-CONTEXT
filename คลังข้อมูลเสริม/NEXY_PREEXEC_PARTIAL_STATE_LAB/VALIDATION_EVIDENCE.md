# PEPSA Validation Evidence

## Evidence status

- E0 Presence: **PASS** for the PEPSA project files on GitHub.
- E1 Static: **PASS** for the executable source/test content bound below.
- E2 Unit/behavior: **PASS** for the executable source/test content bound below.
- E3 Integration with NEXY: **NOT_VERIFIED / OUT OF SCOPE**.
- E4 NEXY user-flow: **NOT_VERIFIED / OUT OF SCOPE**.
- E5 Runtime/operational NEXY behavior: **NOT_VERIFIED / OUT OF SCOPE**.
- E6 Deployment: **NOT_VERIFIED / OUT OF SCOPE**.

## Exact source binding

Repository: `goif74945-crypto/AI-CONTEXT`  
Branch used for authoring: `ai/pepsa-20261005-0121`  
Validated source commit: `9a0666abc7fe9b0e391a95548ec64f94b8974a18`

GitHub Actions had **no workflow run for this commit**. No CI PASS is claimed.

Instead, executable/config/example/test files were fetched from the branch with GitHub's repository API and their Git blob SHA-1 identities were compared with the isolated sandbox copies used for execution. The two initially mismatched sandbox files were adjusted to the exact GitHub bytes; their final Git blob identities then matched:

- `src/nexy_pepsa/parser.py` -> `c84d9eca3d146f6a182d469835aed970e4427bae`
- `tests/test_parser.py` -> `e240d825f5ec8e4a79044f0aaed26ab9ec459c76`

All other executable/config/example/test blobs already matched the GitHub revision. See `EXACT_SOURCE_MANIFEST.json`.

## Static gate

Executed in isolated Linux sandbox against the exact-content mirror:

```bash
python3 -m compileall -q src tests
```

Observed: exit 0.

Status: **PASS / E1_STATIC**.

## Unit and negative-path gate

Executed:

```bash
python3 -m unittest discover -s tests -v
```

Observed:

- 34 tests run;
- 34 passed;
- 0 failures;
- 0 errors.

Coverage of behavior includes:

- strict canonical JSON and float rejection;
- strict input parsing;
- unknown-field rejection;
- non-NFC and ASCII-control-character rejection;
- boolean/integer confusion rejection;
- deterministic lexical topological order;
- duplicate/missing/self/cyclic dependency rejection;
- protected-resource mutation freeze;
- unauthorized-boundary freeze;
- mutation postcondition/evidence gates;
- rollback consistency;
- external-effect idempotency metadata;
- irreversible approval semantics;
- non-terminal irreversible mutation freeze;
- unsafe residual partial-state detection;
- plan-size bound;
- CLI exit semantics;
- 120 permutations of five independent steps producing identical semantic identity/order;
- 128-step DAG behavior.

Status: **PASS / E2_UNIT** for the declared prototype behavior.

## End-to-end prototype validation script

Executed:

```bash
./scripts/run_validation.sh
```

Observed terminal summary:

```text
VALIDATION_GATE=PASS
SAFE_VERDICT=READY
UNSAFE_VERDICT=FREEZE
SAFE_COMBINED_HASH=1cdc74580532368dbb21fbf7a628f166897a438e03bbb7bbaff937147ef7d0ea
UNSAFE_COMBINED_HASH=cb6130cdbb587a04f3a0a21fde7edf07df0d7540526bf43458cd8d0b6bdc59d4
```

The validation script also asserts that the unsafe report contains `PROTECTED_RESOURCE_MUTATION`.

## Package smoke

Environment:

- CPython `3.13.5`
- Linux `6.18.44-x86_64` / glibc 2.41

Executed:

```bash
python3 -m pip install --no-deps --no-build-isolation . -t /tmp/pepsa_install_exact
PYTHONPATH=/tmp/pepsa_install_exact \
  python3 -m nexy_pepsa.cli analyze \
  --plan examples/safe_plan.json \
  --policy examples/policy.json
```

Observed:

- package install: success;
- installed CLI verdict: `READY`;
- installed combined hash: `1cdc74580532368dbb21fbf7a628f166897a438e03bbb7bbaff937147ef7d0ea`.

Status: **PASS** for packaging/import/CLI smoke in this sandbox.

## Important limitations

This evidence does **not** prove:

- authentic approval IDs;
- that a declared rollback handler works;
- that external providers honor idempotency keys;
- correct canonicalization of real repository/API resource aliases;
- absence of TOCTOU between preflight and execution;
- integration with NEXY CORE/LAW/JUDGE/RUN;
- production security or deployment readiness.

Those remain explicit promotion gates in `INTEGRATION_PROPOSAL.md`.
