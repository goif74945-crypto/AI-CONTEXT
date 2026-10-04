# C2 — Emergent Capability Risk Analyzer (ECRA)

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## Objective
Find hazards that arise only when multiple tool steps are connected, even if each step considered alone appears harmless.

## Model
Artifacts carry explicit taints:
- `SECRET`
- `PRIVATE`
- `UNTRUSTED`
- `LOW_TRUST_AUTHORITY`
- `VERIFIED`

Steps consume artifacts, may transform taints through declared capabilities, and produce new immutable artifact names.

Sink findings:
- `E_SECRET_EGRESS`
- `E_PRIVATE_PUBLICATION`
- `E_UNTRUSTED_EXECUTION`
- `E_UNTRUSTED_PROTECTED_MUTATION`
- `E_CONFUSED_DEPUTY`

Transform capabilities:
- secret/private redaction;
- untrusted-data validation;
- authority validation.

## Invariants
- no consumption of an artifact that does not exist;
- no overwriting an existing artifact;
- no duplicate ids/list entries;
- unknown taints/capabilities are rejected;
- findings freeze the plan;
- result includes deterministic trace + fingerprint.

## Critical authority boundary
A capability label is a **claim supplied by the caller**, not proof that a tool really sanitizes or validates. Production adoption must bind capability labels to independently verified tool contracts and versions. Otherwise a lying `VALIDATE_UNTRUSTED` label could erase risk on paper while the real tool remains unsafe.

## Why NEXY could benefit
NEXY coordinates external models and tools. Composition can create a capability none of the tools exposes alone, such as read-secret → transform → network-send or untrusted-input → generated-script → executor. This analyzer provides a deterministic pre-execution dataflow gate.

## Code / tests
- Code: `src/nexy_aux/emergence.py`
- Tests: `tests/test_emergence.py`, `tests/test_properties.py`, `tests/test_hardening.py`
- Cross-concept integration: `src/nexy_aux/integration.py`, `tests/test_integration.py`
