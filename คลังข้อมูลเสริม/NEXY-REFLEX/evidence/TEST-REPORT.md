# NEXY-REFLEX Verification Evidence

## Evidence identity
- mission: `NXR-20261005-0137-REFLEX`
- tested source bundle: `sha256:657b2e62ebdae0d5100420b9dbada1d5b0e071f090ea1b3e29935074b99ae953`
- environment: isolated local container available to this ChatGPT execution
- Python: `Python 3.13.5`
- runtime dependencies: none beyond Python standard library

## E1 — Static validation

### Command
`python -m compileall -q src tests`

### Result
**PASS** — exit code 0.

JSON syntax validation was also executed for every file under `contracts/*.json` and `examples/*.json` using `python -m json.tool`.

Package construction was executed with:

`python -m pip wheel . --no-deps --no-build-isolation`

Result: **PASS**; wheel `nexy_reflex-0.1.0-py3-none-any.whl` was produced in the isolated test environment.

## E2 — Unit/regression validation

### Command
`PYTHONPATH=src python -m unittest discover -s tests -v`

### Result
**PASS — 23/23 tests**.

Coverage includes:
- canonical key-order stability;
- non-finite JSON rejection;
- deterministic digest format;
- PASS path;
- list-order invariant decision digest;
- higher-authority shadowing;
- same-highest-authority conflicting value freeze;
- same-highest-authority same value but different normative obligation freeze;
- stale evidence rejection;
- evidence-class non-substitution;
- explicit current FAIL propagation;
- unknown authority blocking;
- duplicate requirement ID blocking, including identical duplicate definitions;
- orphan evidence blocking;
- dependency cycle blocking;
- deferred/non-current non-gating behavior;
- requirement change transitive invalidation;
- target identity change invalidation;
- diff digest order invariance;
- unsupported contract version rejection;
- invalid scope rejection;
- invalid evidence class rejection.

## CLI behavior checks
- PASS snapshot: exit `0`, verdict `PASS`, action `ACCEPT_ADVISORY`.
- Conflict snapshot: exit `2`, verdict `CONFLICT`, action `FREEZE_RECOMMENDED`.
- Matching replay digest: exit `0`, `replay_match=true`.
- Wrong replay digest: exit `3`.
- Malformed JSON: exit `4` with `INPUT_ERROR`.
- Target revision change: impact report invalidated all evidence tied to the affected requirement set in the example.

## Defects found and repaired during verification

### D1 — order-sensitive digest
Initial unit run found that reordering requirement/evidence arrays changed `input_digest` and `decision_digest`.

Repair: introduced semantic snapshot normalization that sorts order-insensitive collections while preserving authority precedence order.

Regression evidence: dedicated order-invariance tests now PASS.

### D2 — conflict hidden by dependency cascade
Initial unit run found that a top-authority conflict could remove an effective claim, causing a downstream missing-dependency `BLOCKED` verdict to hide the primary `CONFLICT`.

Repair: structural corruption still returns early as `BLOCKED`; after structure passes, top-authority `CONFLICT` outranks cascade blockers caused by unresolved authority.

Regression evidence: top-authority conflict test now returns `CONFLICT`.

### D3 — hardening after first green run
Independent review identified three cases not caught by the first suite:
- identical duplicate IDs were still accepted;
- equal value at equal authority could collapse claims with different evidence/scope/dependency obligations;
- impact digests were still list-order-sensitive.

Repair: enforce unique IDs unconditionally, compare full normative signatures, and reuse semantic snapshot digests in impact analysis.

Regression evidence: three additional tests plus unknown-scope validation added; final suite is 23/23 PASS.

## Evidence boundary
This evidence proves static/package properties and unit-level behavior of the exact source bundle identified above. It does **not** prove NEXY runtime integration, deployment behavior, production security, or NEXY implementation correctness.

## Remaining verification before mission completion
GitHub write + read-back must confirm that repository content hashes match `evidence/source-manifest.sha256`. Until that read-back succeeds, repository delivery status is **NOT_VERIFIED**.
