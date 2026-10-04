# NEXY Five Forge — 2026-10-05

Standalone research-and-implementation package created under the AI-CONTEXT supplemental-data boundary.

## Mission
Create five non-colliding, testable systems that could integrate with NEXY.AI later without modifying the NEXY.AI implementation repository.

## Status classes
- Design: PROPOSED_BY_AI unless explicitly promoted by project authority.
- Prototype code: STANDALONE / SANDBOX ONLY.
- Integration with NEXY.AI: NOT PERFORMED.
- NEXY.AI runtime effect: NONE.

## Systems
1. Context Budget Optimizer (CBO) — deterministic context packing under token budgets with authority/relevance/freshness weighting and dependency closure.
2. Tool Evidence Router (TER) — chooses the lowest-cost bounded tool route that can satisfy evidence-class and capability constraints.
3. Recovery Recipe Distiller (RRD) — converts repeated verified failure/repair episodes into reusable recovery recipes while preserving evidence and failure penalties.
4. Skill Compiler (SKC) — promotes repeated successful execution traces into portable skills only when consistency, evidence and secret-safety gates pass.
5. Assumption Burn-down Planner (ABP) — selects the smallest validation probe set needed to eliminate high-risk assumptions before mutation.

## Design law
Every system is deterministic for the same normalized input, explicit about failure/freeze states, dependency-aware, provenance-preserving, and usable without model-private reasoning.

## Verification
Each system has executable Python unit tests. The aggregate suite is runnable with:

```bash
python -m unittest discover -s tests -v
```

See `EVIDENCE.md` for observed results from the sandbox run associated with this package.
