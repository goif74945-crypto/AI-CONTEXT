# NEXY Trust UX Contract Lab

**Status:** AI-PROPOSED / ADVISORY / REFERENCE IMPLEMENTATION  
**Storage target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม`  
**Protected target:** any repository whose name contains `NEXY.AI` is READ-ONLY for this work  
**Session reference:** `CHAT-20261005-0121-NEXY-TRUST-UX-CONTRACT-LAB`  
**Actual ChatGPT platform conversation ID:** UNKNOWN / not exposed to the available tool surface

## Purpose

This lab explores one narrow product problem that is easy to underestimate: how NEXY can expose strict backend truth to a human without allowing the presentation layer to invent success, hide FREEZE, imply authority, or overwhelm the operator with internal machinery.

The lab produces a deterministic **Trust Card compiler**. It accepts an already-authoritative backend envelope and role, then emits a presentation contract. It does not decide system truth, release policy, authorization, or recovery. Those remain backend/Core/Law responsibilities.

## Why this is useful

NEXY's source-derived context repeatedly requires:

- core hidden, useful truth visible;
- one released result or explicit freeze;
- frozen system must look frozen;
- loading/pending UI must not imply success;
- `visible ≠ editable ≠ executable`;
- role visibility must not substitute for backend authorization;
- FREEZE surfaces must expose incident, trigger, blocking layer, and recoverability;
- the user should understand the next legal action without learning the entire internal architecture.

This lab turns those principles into a small executable contract that future NEXY UI work can compare against.

## Deliverables

- `00_TASK_CONTRACT.md` — scope, authority, acceptance criteria.
- `01_TEMP_MEMORY.md` — resumable execution checkpoint.
- `02_SOURCE_ALIGNMENT.md` — source facts vs proposals.
- `03_TRUST_UX_CONTRACT.md` — deterministic presentation model.
- `04_FREEZE_COMMUNICATION_PROTOCOL.md` — exact FREEZE/STOP/HOLD behavior.
- `05_ACTION_VISIBILITY_AND_AUTHORITY.md` — action/role boundary.
- `06_AI_PROPOSED_FUTURE_SYSTEMS.md` — explicitly non-authoritative future ideas.
- `schemas/trust-card.schema.json` — machine-readable proposal schema.
- `reference_impl/trustux.py` — dependency-free Python reference compiler.
- `tests/test_trustux.py` — behavioral unit suite.
- `fixtures/*.json` — reproducible cases.
- `VALIDATION_REPORT.md` — evidence captured from executed tests.
- `FINAL_AUDIT.md` — final requirement/evidence audit.

## Authority boundary

Everything in this folder is **secondary advisory context**. It cannot override DOC-B, DOC-C, DOC-D where authoritative, current implementation truth, runtime evidence, or explicit user directive.

The code is a reference model, not proof that NEXY currently implements this behavior.
