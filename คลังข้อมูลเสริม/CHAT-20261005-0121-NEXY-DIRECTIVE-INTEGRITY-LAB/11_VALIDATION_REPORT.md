# Validation Report

Status: PASS FOR STANDALONE REFERENCE SCOPE
Date: 2026-10-05 (+07:00)
Session: `NEXY-DIRECTIVE-INTEGRITY-20261005-0121-SOL`

## Claims and evidence

### E1 — Python static compile
Command: `python -m py_compile reference/directive_integrity.py reference/test_directive_integrity.py`  
Observed exit: `0`  
Status: PASS.

### E1 — JSON Schema
Validator: Python `jsonschema` 4.26.0 / Draft 2020-12.  
Schema self-check: PASS.  
Validated fixtures: `parent.json`, `child-safe.json`, `child-broadened.json`, `authorization-scope-expand.json`.  
Observed: all PASS.

### E2 — Unit behavior
Command: `cd reference && python -m unittest -v test_directive_integrity.py`  
Observed: `Ran 22 tests` / `OK` / process exit `0`.  
Status: PASS.

Coverage includes positive refinement, unauthorized scope/action/target/side-effect/mutation changes, authority loss, constraint loss, ambiguity laundering, risk downgrade, parent binding, deterministic set ordering, explicit re-authorization, malformed data, operator explanation, mapping stability, and CLI exit semantics.

### E2 — Fixture CLI: safe refinement
Command: `python reference/directive_integrity.py compare fixtures/parent.json fixtures/child-safe.json`  
Observed status: `PASS`; exit `0`.

### E2 — Fixture CLI: adversarial broadening
Command: `python reference/directive_integrity.py compare fixtures/parent.json fixtures/child-broadened.json`  
Observed status: `FREEZE`; exit `2`.  
Observed violations: `MUTATION_ESCALATED`, `SCOPE_BROADENED`, `SIDE_EFFECT_ADDED`.

## Deterministic fixture identities
Parent snapshot digest: `b026d594fb62d0060dff9d3adbe945d1668e738d2d54c8e3bd69330caf12f3c8`.  
Safe fixture result child digest: `e39c683ff9b4d3226c0751b7d27e9c57b4bf694e055d0bc1ac515afa300dacce`.  
Broadened fixture result child digest: `e4d2ff2b82bf95f164087041ce512db3ac8d5af7e835472f2e936a76ae90d738`.

## Evidence limitations
This proves the standalone Python model at E1/E2 only. It does not prove NEXY production integration, API/DB behavior, browser behavior, operational reliability, security containment, deployment, or physical-system behavior. Those remain NOT_VERIFIED because this session intentionally made no NEXY implementation changes.

## Publication verification rule
After GitHub publication, re-fetch the exact committed copy. Prefer rerunning the downloaded code at the exact AI-CONTEXT commit so repository-hosted bytes, not merely the pre-upload local workspace, receive E2 evidence.
