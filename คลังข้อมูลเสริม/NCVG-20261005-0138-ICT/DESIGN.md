# NCVG Design

> **Classification:** AI PROPOSAL / EXPERIMENTAL COMPANION. Not canonical NEXY.AI requirement.

## Objective
Create a deterministic external gate that makes completion claims mechanically harder to fake by enforcing cross-record consistency between task scope, requirements, evidence, execution status, and mutation boundaries.

## Authority
NCVG consumes authoritative artifacts; it does not create authority. User Law and canonical NEXY specifications outrank NCVG policy.

## Scope
In scope: semantic JSON validation, deterministic hashing, ALLOW/FREEZE, evidence-class admission, exact-commit binding, protected-scope checks, standalone CLI/API.

Out of scope: editing NEXY.AI repositories, deciding NEXY product law, deployment/physical verification, secrets, organizational signatures, or treating ALLOW as deployment safety.

## Core invariants
1. Missing mandatory proof never yields ALLOW.
2. Mandatory requirements require referenced PASS evidence.
3. Evidence-class substitution is never implicit.
4. `expected_commit` is exact when configured.
5. Protected/forbidden mutation claims yield FREEZE.
6. Canonical JSON identity is deterministic.
7. Canonicalization failure yields FREEZE.
8. NCVG never performs mutations.
9. ALLOW means only that the supplied bundle satisfies the supplied NCVG policy.

## Modules
- `canonical.py`: canonical JSON + SHA-256
- `model.py`: finding/decision/status model
- `validator.py`: semantic admission
- `gate.py`: fail-closed aggregation
- `cli.py`: stable command/exit interface

## State machine
`INPUT -> CANONICALIZE -> VALIDATE -> ADMIT_EVIDENCE -> CHECK_MUTATIONS -> DECIDE`

Any blocking finding -> `FREEZE`.

## Compatibility
Runtime code uses the Python standard library only and plain JSON. This is intentionally provider/model independent. AI-CONTEXT schemas should remain an earlier structural-validation stage in any production pipeline.
