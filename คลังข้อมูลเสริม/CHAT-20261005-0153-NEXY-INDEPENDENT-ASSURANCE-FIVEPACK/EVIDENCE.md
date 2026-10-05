# Evidence — NEXY Independent Assurance Five-Pack

## Evidence boundary
These results prove the standalone reference implementation in this execution environment. They do **not** prove behavior inside the NEXY.AI implementation, production deployment, or adoption into governing NEXY law.

## Source/context evidence used for design compatibility
The work was bootstrapped from `AI-CONTEXT/INDEX.md`, `AI-EXECUTION-KERNEL.md`, global security/verification rules, NEXY overview/current 837-row source matrix, and relevant deep context on SWARM/JUDGE, capability governance, human control surfaces, DOC-C and final architecture. Existing sibling names under `คลังข้อมูลเสริม/` were inspected to reduce direct duplication. The five candidate collision searches returned no direct matches for the exact candidate themes. This is collision screening, not a mathematical proof that no semantically related work exists anywhere.

## TDD / repair trace
1. Initial test execution failed at import because `src/` was not on the module path. This was classified as harness failure, not product failure.
2. Harness was corrected using `PYTHONPATH=src`; the RED run then correctly failed because the five implementation modules did not yet exist.
3. After implementation, `unittest discover` returned zero tests because the suite used pytest-style test functions. That run was explicitly rejected as non-evidence.
4. Runner was corrected to pytest and the first valid GREEN run passed 15 tests.
5. Negative, edge, cross-module and determinism tests were added; the expanded package reached 31 then 35 passing tests.
6. A compact standalone artifact was created for durable persistence. The exact persisted code/test pair was then re-tested independently: 32 tests passed.

## Fresh decisive proof for the exact persisted bundle
Command:

`PYTHONPATH=. python -m pytest -q`

Observed in `FINAL_TEST.txt`:

`43 passed in 0.06s`

`EXIT_CODE=0`

## Static proof for the exact persisted bundle
Command:

`PYTHONPATH=. python -m compileall -q nexy_assurance_fivepack.py test_nexy_assurance_fivepack.py`

Observed in `STATIC.txt`:

`COMPILE_EXIT=0`

Runtime: Python 3.13.5 was used in the larger local package verification. No claim is made for untested Python implementations or platforms.

## Continuation iteration — AIG critical-severity escalation integrity
The highest-value verified weakness found in the package was an AIG ordering defect: when an alert changed from `LOW`, `MEDIUM` or `HIGH` to `CRITICAL` while retaining the same semantic key, evidence fingerprint and state fingerprint, duplicate suppression ran before severity escalation was recognized and returned `SUPPRESS`.

Design invariant added: escalation from any noncritical severity to `CRITICAL` is material and must be delivered even when the state and evidence fingerprints are unchanged. Exact repeated `CRITICAL` alerts remain eligible for duplicate suppression.

RED command:

`PYTHONPATH=. python -m pytest -q test_nexy_assurance_fivepack.py::test_aig_escalation_to_critical_never_suppressed_as_duplicate`

Observed before implementation: `LOW -> CRITICAL` returned `SUPPRESS`; pytest reported `1 failed`.

Minimal implementation: AIG now checks noncritical-to-`CRITICAL` escalation before exact-duplicate suppression and returns `DELIVER / critical-severity-escalated`.

Fresh targeted proof after repair: `3 passed in 0.05s` across `LOW`, `MEDIUM` and `HIGH` prior severities.

Fresh full regression proof after repair: `35 passed in 0.05s`; exit code 0.

Fresh static proof after repair: Python 3.12.14 `compileall` exit code 0.

Evidence classification remains E1 for compilation and E2-style local execution for AIG behavior. NEXY.AI integration, runtime operation, deployment and law promotion remain NOT_VERIFIED.

## Continuation iteration — IAQ correlation-metadata completeness
The highest-value verified weakness found in the next audit was that `AgentVote` accepted missing or blank independence metadata. A vote with an empty provider, model family, data lineage or toolchain fingerprint could reach correlation clustering even though IAQ cannot establish its failure-domain independence from incomplete metadata.

Design invariant added: provider, model-family, data-lineage and toolchain metadata must be complete and nonblank; unknown correlation metadata cannot be counted as independent evidence.

RED command:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -m pytest -q test_nexy_assurance_fivepack.py::test_iaq_missing_independence_metadata_rejected`

Observed before implementation: all five parameterized cases failed because no `ValueError` was raised (`5 failed`).

Minimal implementation: `AgentVote.__post_init__` now rejects missing/blank provider, model family, toolchain fingerprint, empty data lineage, and blank/non-string lineage entries before any quorum clustering occurs.

Fresh targeted proof after repair: `5 passed in 0.05s`.

Fresh full regression proof after repair: `40 passed in 0.06s`; exit code 0.

Fresh static proof after repair: Python 3.12.14 `compileall` exit code 0.

Evidence classification remains E1 for compilation and E2-style local execution for IAQ validation behavior. Authenticated metadata provenance, NEXY.AI integration, runtime operation, deployment and law promotion remain NOT_VERIFIED.

## Continuation iteration — RAAS exact-boolean control validation
The highest-value verified weakness found in the next audit was that `ActionRisk` trusted Python type hints for its three control flags without runtime validation. Truthy substitutes could change safety routing; specifically, `compensation_available="false"` is truthy in Python and could prevent the default irreversible/high-impact/no-compensation FREEZE path.

Design invariant added: production, permission-change and compensation-availability inputs must be exact booleans; truthy/falsy substitutes are invalid and cannot alter assurance routing.

RED command:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -m pytest -q test_nexy_assurance_fivepack.py::test_raas_non_boolean_control_flags_rejected`

Observed before implementation: all three parameterized cases failed because no `ValueError` was raised (`3 failed`).

Minimal implementation: `ActionRisk.__post_init__` now requires exact `bool` instances for all three control flags before scoring or routing.

Fresh targeted proof after repair: `3 passed in 0.05s`.

Fresh full regression proof after repair: `43 passed in 0.06s`; exit code 0.

Fresh static proof after repair: Python 3.12.14 `compileall` exit code 0.

Evidence classification remains E1 for compilation and E2-style local execution for RAAS validation behavior. Policy calibration, NEXY.AI integration, runtime operation, deployment and law promotion remain NOT_VERIFIED.

## Coverage intent
The compact suite contains tests for:
- IAQ correlated replicas, fake quorum, independent failures, empty input, duplicate identity, correlation-metadata completeness and order invariance;
- ECG clean roots, target-derived oracle, shared untrusted/trusted roots, cycles, direct overlap and edge-order invariance;
- RAAS low risk, high-risk production promotion, irreversible/no-compensation freeze, permission changes, invalid scales, exact-boolean controls and repeatability;
- CTR retirement, stale/future snapshots, explicit restore, replacement, invalid self-replacement and canonical digest ordering;
- AIG duplicate suppression, changed critical delivery, exact critical duplicate suppression, noncritical budget, evidence changes and time regression;
- one integrated high-risk flow across all five mechanisms.

## Evidence classification
- code presence/content: E0;
- Python compilation: E1;
- module behavior: E2-style local execution;
- cross-module standalone flow: local E3-like package interaction only;
- NEXY implementation integration: NOT_VERIFIED;
- NEXY E2E/runtime/operational behavior: NOT_VERIFIED;
- NEXY deployment: NOT_VERIFIED.

## Truth constraints
A passing standalone test does not establish adoption, compatibility with an unknown future NEXY HEAD, production security, calibrated risk scoring, correctness of supplied provenance metadata, or deployment readiness. Those claims require separate evidence.

## Remote persistence proof
The base bundle was published through a dedicated branch and PR to avoid overwriting highly concurrent `main` writers. PR #66 merged successfully to `main` with merge commit `a989043468510309a07b9ef7ab8da46c056c4005`.

Post-merge directory read-back from `main` returned exactly the expected eleven base-bundle files. Their Git blob SHAs matched the locally verified Git objects, including:
- `nexy_assurance_fivepack.py` -> `bc37cb0159a6db7e8bdde79c02bc3184e4433e58`;
- `test_nexy_assurance_fivepack.py` -> `6ec709f1ef0636a5fd784dfa7d5580a14bccc4ed`;
- `DESIGN.md` -> `a39e48a9ad4bcb83e3ec111a40d92a5de7fc97ce`;
- original `EVIDENCE.md` base object -> `0390f548476c62e65ece58c2ef0d67278b47425f`;
- original `MANIFEST.sha256` base object -> `87347a1daea387bdd18f2768a13e5fadb933b8f4`.

PR metadata for the base publication reported 11 changed files, 1026 additions and 0 deletions. This proves repository persistence of the standalone package. It still does not prove NEXY.AI runtime integration or deployment.
