# NEXY::PRISM

**Truth-Preserving Progressive Interface State Mapper**

Status: **AI_PROPOSED_CONCEPT / FUTURE_OPTION / NOT_CURRENT_BUILD_REQUIREMENT / PROTOTYPE_ONLY**

NEXY::PRISM is a deterministic presentation-policy compiler proposed as a future supplemental layer for NEXY. It translates already-authoritative backend state into a user-facing control-surface plan while preserving NEXY's truth, evidence, permission, FREEZE, STOP, and release semantics.

PRISM is intentionally **not** CORE, LAW, JUDGE, AUTH, or a release authority. It cannot grant permission, declare an output final, recover a freeze, or mutate system state. It can only narrow the visible/interactive surface.

## Why it exists

Strict systems often become unpleasant to use because every screen exposes every internal detail. The opposite failure is worse: attractive UI hides risk, uncertainty, blocked state, or authority boundaries. PRISM introduces a deterministic middle layer:

`AUTHORITATIVE BACKEND STATE -> PRISM -> MINIMUM SAFE CONTROL SURFACE`

The user can prefer compact or deep detail, but preference is bounded by a **truth floor**. Critical risk, FREEZE, STOP, irreversible actions, conflicts, and unverified evidence automatically raise the minimum detail level.

## Core invariants

1. Backend authorization is authoritative. PRISM may deny more, never allow more.
2. Release authorization is authoritative. PRISM never infers release from confidence or appearance.
3. FREEZE and STOP are visually mandatory and fail closed.
4. A user preference may raise detail but cannot suppress mandatory disclosures.
5. Irreversible actions require typed confirmation.
6. Role-facing capability rules are defense-in-depth, not backend authorization.
7. Contradictory release flags compile to `CONTRACT_CONFLICT` with actions disabled.
8. Identical canonical input produces identical output and SHA-256 fingerprint.

## Prototype package

- `nexy_prism/model.py` — typed input/output contracts.
- `nexy_prism/compiler.py` — deterministic compiler.
- `nexy_prism/policy.py` — surface capability restrictions.
- `nexy_prism/canonical.py` — canonical JSON + fingerprint.
- `nexy_prism/invariants.py` — executable safety/truth invariants.
- `tests/test_compiler.py` — focused behavior tests.
- `tests/test_exhaustive_matrix.py` — 430,080-scenario cross-product invariant test.
- `schema/surface-input.schema.json` — machine-readable input schema.

## Verification

Run from this directory:

```bash
python -m compileall -q nexy_prism tests examples
python -m unittest discover -s tests -v
python examples/demo.py
```

The verification report records the actual observed result for the exact prototype stored here.
