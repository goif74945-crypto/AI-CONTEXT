# NEXY Lo4 Frontier Five

**Status:** isolated prototype suite, `Lo4_AI_PROPOSAL_ONLY`  
**Conversation code:** `CHAT-20261005-0221-NEXY-LO4-FRONTIER-FIVE`  
**Target:** supplemental research under `goif74945-crypto/AI-CONTEXT` only.

This project contains five AI-proposed systems designed to be compatible with NEXY.AI principles without claiming Canon, current-build, runtime, deployment, or product promotion.

## Five systems

1. **Counterfactual Authority Wind Tunnel (CAWT)** — replays decision cases under baseline vs candidate authority rules before a law/policy change is adopted; freezes on dangerous authority expansion or introduced conflicts.
2. **Epistemic Debt & Evidence Decay Ledger (EDEL)** — detects when evidence becomes stale after subject versions change and propagates proof debt through dependent claims.
3. **Capability Composition Firewall (CCF)** — detects emergent privilege escalation that appears only when multiple individually permitted capabilities are composed.
4. **Shadow Invariant Miner & Falsifier (SIMF)** — mines candidate invariants from successful traces, labels them proposal-only, and actively tries to falsify them before any possible promotion.
5. **Deterministic Replay Capsule & Differential Oracle (DRCDO)** — binds request/state/policy/tool versions/seed into a replay capsule and detects output divergence or executor faults across implementations/providers/adapters.

## Cross-system promotion gate

`integration.py` combines all five outputs. Any critical risk freezes the candidate. A local PASS still means only: "the isolated prototype gate found no configured blocker." It does **not** authorize Canon promotion.

## Evidence achieved in this isolated workspace

- E1: Python AST/compile validation PASS.
- E2: 27 unit/negative/determinism tests PASS.
- E3: two cross-module integration scenarios PASS.
- Determinism stress: 40,000 checks PASS across four fixed seeds.
- Secret-pattern scan: no configured credential patterns found.
- Package build: wheel built; digest recorded in `evidence/wheel-sha256.txt`.

NEXY implementation/runtime/deployment integration remains **NOT_VERIFIED**.

## Reproduce

```bash
PYTHONPATH=src python -m compileall -q src tests tools
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python tools/stress_determinism.py 2000
PYTHONPATH=src python tools/static_audit.py
python -m pip wheel . -w dist --no-deps --no-build-isolation
```

## Scope boundary

No repository whose name contains `NEXY.AI` is modified by this work. The suite is a research/prototype artifact stored only in AI-CONTEXT.
