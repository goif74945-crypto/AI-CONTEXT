# NEXY Lo4 Coherence & Utility Lab

**Classification:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL`  
**Durable work code:** `CHAT-20261005-0222-NEXY-LO4-COHERENCE-UTILITY-LAB`

This standalone reference lab explores five systems intended to improve future NEXY coherence and user value without granting any AI-generated proposal authority over NEXY Canon.

1. **BKR — Bitemporal Knowledge Reconstructor:** answers two different questions explicitly: what was valid in the world at time `t`, and what evidence was known to the system by time `k`.
2. **CEML — Concurrent Epistemic Merge Lattice:** merges append-only claim replicas deterministically, preserving tombstones and unresolved equal-authority conflicts rather than silently selecting a winner.
3. **CUVL — Causal User Value Ledger:** converts an innovation claim into a testable mechanism → user outcome → primary metric → guard metric → falsifier contract and evaluates evidence without converting advisory evidence into Canon.
4. **STCE — Scoped Terminology Contract Engine:** resolves terms by explicit scope and blocks same-scope definition/alias ambiguity so overloaded words cannot become hidden guessing surfaces.
5. **FSA — Failure Semantics Algebra:** composes NEXY-style statuses using an explicit fail-closed precedence model and blocks locally passing nodes whose required dependencies are unresolved.

## Local verification

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py' -v
```

The reference code uses the Python standard library only and performs no network, model, subprocess, secret, or production operations.

## Evidence boundary

A local PASS proves only the standalone reference behavior tested here. It does **not** prove NEXY.AI integration, production safety, deployment, performance, security hardening, or Canon promotion.
