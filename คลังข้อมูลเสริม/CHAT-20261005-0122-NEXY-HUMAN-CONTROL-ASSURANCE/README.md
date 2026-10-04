# NEXY Human Control Surface Assurance (HCAS)

**STATUS: AI-PROPOSED ADVISORY TOOLING. NOT A NEXY.AI REQUIREMENT. NOT NEXY.AI IMPLEMENTATION EVIDENCE.**

HCAS is a deterministic, zero-dependency linter for machine-readable descriptions of NEXY-facing control surfaces. It exists to catch a specific class of product-integrity bugs before UI polish disguises them: a control that looks authoritative but lacks backend authorization, a loading state presented as success, a hidden/maskable FREEZE state, or a destructive action without explicit confirmation/audit/failure semantics.

## Why this is distinct
This repository already contains advisory work on Human Authority, Scope Firewall, semantic contracts, evidence and capability negotiation. HCAS does not replace them. It sits at the **human-control-surface boundary** and checks whether a UI/action manifest preserves those laws when they become product controls.

## Project facts used as inputs
`FACT_PROJECT` from AI-CONTEXT NEXY deep context:
- UI visibility is never backend authorization.
- dangerous actions require an explicit confirmation/authority path.
- the UI may not hide/mask authoritative FREEZE.
- mobile freeze banner remains sticky.
- loading animation is not evidence that execution succeeded.
- UI should reflect real state and one action should have one defined result.

Those facts are provenance inputs only. HCAS's exact manifest fields and lint rules are **PROPOSAL** unless separately promoted by NEXY authority.

## Quick run
```bash
PYTHONPATH=src python -m hcas.cli examples/safe_manifest.json --pretty
PYTHONPATH=src python -m hcas.cli examples/unsafe_manifest.json --pretty
python scripts/run_checks.py
```

Expected CLI behavior:
- safe manifest: exit `0`, status `PASS`;
- unsafe manifest: exit `2`, status `FAIL`;
- unreadable/invalid JSON: exit `64`.

## Profiles
- `current_vnext`: conservative checks directly motivated by current NEXY project/product context plus explicitly labeled advisory structure.
- `strict_future`: AI-proposed harder profile that additionally requires dual approval for destructive/privilege-changing actions. It is **not current law**.

## Trust boundary
HCAS does not grant permission, execute actions, authorize users, validate a live backend, or prove UI behavior. It validates a manifest. Runtime/UI claims still require E3/E4/E5-class evidence as appropriate.
