# NEXY Proof Capsule Compiler — PROPOSAL ONLY

Stored in AI-CONTEXT as advisory research. It does **not** change NEXY.AI source, law, or build scope.

Purpose: turn a large claim/evidence set into a small deterministic proof capsule while refusing to hide unresolved conflict, stale/wrong-version proof, evidence-class mismatch, or proof omitted merely to fit a UI/token budget.

Core properties: exact evidence classes; exact target/version; explicit `as_of`; authority-before-compression; equal-authority material conflict => FREEZE; weaker dissent disclosure; SHA-256 evidence digest required by default; canonical input commitment; deterministic incremental cover; fail-closed item/cost budgets; no third-party dependencies.

Run: `python -m unittest -v test_proof_capsule.py`

Authority: SECONDARY / ADVISORY only. Production adoption requires explicit authoritative promotion and fresh integration/runtime evidence.
