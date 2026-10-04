# NEXY Failure Witness Minimizer (NFWM)

**Status: AI-PROPOSED EXTERNAL RESEARCH PROTOTYPE — NOT PART OF NEXY.AI**

NFWM is an isolated tool for turning a large NEXY-style execution trace that violates a known invariant into a small, deterministic, replayable failure witness.

It is intentionally stored outside the `NEXY.AI-` repository. It does not mutate, import from, deploy to, or claim runtime authority over NEXY.AI.

## Why this exists

Large incident traces are expensive to inspect and easy to misread. NEXY's current project context emphasizes deterministic state transitions, explicit FREEZE semantics, idempotency, incident linkage, evidence discipline, and replayable verification. NFWM applies those ideas to **external trace analysis**:

`TRACE → STRICT PARSE → INVARIANT CHECK → FAILURE CLASS → DETERMINISTIC DDMIN → 1-MINIMAL WITNESS → HASH → REPLAY VERIFY`

The resulting witness is useful for:

- debugging without scanning the full trace repeatedly;
- attaching a compact reproducer to an incident;
- regression-fixture generation;
- comparing failures across builds without pretending that one witness proves the whole system;
- reducing unnecessary log exposure when a small event subset is sufficient.

## Implemented invariants

The v0.1 profile checks:

1. `INV_SEQUENCE_STRICT_INCREASE` — event sequence must strictly increase.
2. `INV_TRANSITION_SHAPE` — transition events require source and destination states.
3. `INV_FSM_TRANSITION` — transition must exist in the configured allowed-transition set.
4. `INV_FREEZE_INCIDENT_LINK` — entering `FREEZE` requires an incident identifier.
5. `INV_STOP_TERMINAL` — no state transition may leave `STOP`.
6. `INV_RELEASE_AFTER_FREEZE` — release may not occur after `FREEZE` in the same trace/run scope.
7. `INV_IDEMPOTENCY_REUSE` — one idempotency key may not start different run IDs.

These are **profile-level checks derived from AI-CONTEXT project context**, not evidence that the live NEXY implementation currently emits these exact event records.

## Determinism rules

- Python standard library only at runtime.
- Canonical JSON uses UTF-8, sorted keys, no insignificant whitespace, and rejects NaN/Infinity.
- Witness hash is SHA-256 of canonical event JSON.
- No system clock, RNG, network access, AI model call, or hidden adaptive behavior participates in analysis/minimization.
- Minimization is explicitly `DETERMINISTIC_1_MINIMAL`, not a claim of globally minimum cardinality.

## Quick start

```bash
cd <NFWM_ROOT>
PYTHONPATH=src python -m unittest discover -s tests -v

PYTHONPATH=src python -m nfwm.cli analyze \
  tests/fixtures/release_after_freeze.json \
  --profile profiles/nexy-vnext-trace-profile.json \
  --minimize

PYTHONPATH=src python -m nfwm.cli verify-witness \
  evidence/sample-witness.json \
  --profile profiles/nexy-vnext-trace-profile.json
```

Exit codes:

- `0` = analysis PASS or witness verification PASS.
- `2` = trace parsed correctly and one or more invariant violations were found.
- `3` = witness verification failed.
- `64` = invalid input/profile/IO/contract failure.

## Source authority used

Current AI-CONTEXT material used for design:

- `AI-EXECUTION-KERNEL.md`
- `rules/GLOBAL.md`
- `rules/SECURITY.md`
- `rules/VERIFICATION.md`
- `projects/NEXY.AI/overview.md`
- `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`
- `projects/NEXY.AI/deep/doc-c-vnext-build-spec.md`
- `projects/NEXY.AI/deep/doc-e-deployment-evidence.md`

The historical 215-entry registry was not used.

## Scope warning

NFWM is not:

- a NEXY production component;
- a replacement for DOC-E deployment evidence;
- a proof that NEXY.AI runtime behavior matches the profile;
- an authorization mechanism;
- an incident-response system;
- a globally optimal delta debugger.

See `00_TASK_CONTRACT.md`, `01_DESIGN.md`, `02_REQUIREMENT_LEDGER.md`, and `evidence/TEST_RESULTS.md` for exact boundaries and executed proof.
