# 01 — Cross-Modal Truth Lattice (CMTL)

Status: **AI-PROPOSED REFERENCE SYSTEM — NOT CANONICAL NEXY LAW**

Purpose: detect explicit semantic contradictions across structured artifacts such as spec text, code, API, UI, tests, config and runtime observations without using free-form model inference.

Implementation: `../src/cross-modal-consistency.ts`
Tests: `../tests/run-tests.ts`
Evidence: `../EVIDENCE.md`

Key invariants: canonical semantic key; order-invariant report; explicit modality coverage; critical conflicts may only request advisory FREEZE; any real NEXY freeze must pass through canonical LAW/state transition.

Failure model: malformed identifiers or invalid cross-check policy fail closed with `ContractError`; missing cross-modal coverage is surfaced rather than treated as agreement.
