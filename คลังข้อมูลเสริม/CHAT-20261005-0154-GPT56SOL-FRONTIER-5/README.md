# NEXY Frontier-5 Reference Lab

This lab contains five **AI-proposed** systems designed as future-compatible extensions for NEXY.AI. They are intentionally outside the NEXY implementation repository.

## The five proposals

1. **Model Drift Sentinel (MDS)** — fingerprints provider behavior from probe observations and freezes hot-swap acceptance on critical drift.
2. **Semantic Capability ABI Compiler (SCAC)** — compiles provider-specific capability declarations into a provider-neutral deterministic ABI binding plan.
3. **Context Taint Firewall (CTF)** — propagates provenance taint and prevents untrusted/model-generated context from silently becoming authority or leaking secrets.
4. **Effect Transaction Coordinator (ETC)** — provides prepare/commit/compensate semantics for multi-tool side effects, including irreversible-action gates.
5. **Scoped Authority Lease Engine (SALE)** — evaluates temporary, bounded delegated authority with TTL, usage caps, resource/action scope and parent-child non-escalation.

## Important status
These are reference implementations and integration proposals. They do not alter NEXY.AI and do not prove production readiness.

## Reproduce

```bash
python run_all_tests.py
python verify_manifest.py
```

Expected result: all five suites PASS and manifest verification PASS.
