# NEXY Cognitive Assurance Foundry

**Status:** AI-PROPOSED / ADVISORY / NOT CANONICAL NEXY LAW  
**Storage target:** `AI-CONTEXT/คลังข้อมูลเสริม/`  
**Protected scope:** every repository whose name contains `NEXY.AI`

This reference implementation explores five deterministic assurance engines that can be integrated around NEXY without granting them authority over NEXY itself.

## Five concepts

1. **Intent Lattice Compiler (ILC)**: compiles user intent into an explicit authority/scope/evidence contract and freezes on material gaps or protected-scope collisions.
2. **Counterfactual Adoption Gate (CAG)**: evaluates a proposed capability against explicit failure scenarios, residual risk, rollback, evidence plans and invariant preservation before adoption.
3. **Cognitive Debt Ledger (CDL)**: turns assumptions, stale evidence, contradictions, orphan requirements and unverified completion claims into measurable release debt.
4. **Proof Horizon Scheduler (PHS)**: treats evidence as a dependency graph and invalidates/requeues proofs when source/config/upstream proofs drift or exceed freshness budgets.
5. **Human Trust Budget Governor (HTBG)**: chooses the smallest safe interaction burden (execute, explain, confirm, freeze) from uncertainty, evidence, impact, reversibility and scope clarity.

## Integration philosophy

These engines produce advisory decisions and stable SHA-256 fingerprints. They do not mutate project state and do not use clock, randomness, filesystem, environment, network or hidden I/O in their core logic. They are intentionally compatible with a pattern where NEXY::JUDGE remains final authority.

Suggested adapter boundary:

`NEXY request/context -> normalized JSON -> Foundry engine(s) -> advisory Decision -> NEXY::JUDGE -> legal output or freeze`

## Run verification

```bash
python -m compileall -q nexy_caf tests
python -m unittest discover -s tests -v
```

## Evidence boundary

A passing local test proves only this isolated reference implementation under the executed Python environment. It does not prove integration, NEXY runtime behavior, deployment, product UX, or canonical adoption.
