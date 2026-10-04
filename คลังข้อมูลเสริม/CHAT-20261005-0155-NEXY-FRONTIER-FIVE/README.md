# NEXY Frontier Five Supplemental Lab

**Status: AI-proposed concepts with executable isolated reference implementations.**

Execution reference: `ACX-NF5-20261005T0155+0700-01`  
Target repository: `goif74945-crypto/AI-CONTEXT` only.  
NEXY.AI repository mutation: **FORBIDDEN / NOT PERFORMED**.

## Five distinct concepts

1. **UDM — Uncertainty Dependency Mesh**: claim DAG with confidence/freshness propagation, impact closure, and fail-closed decision readiness.
2. **AEC — Ambiguity Experiment Compiler**: chooses safe reversible probes to resolve material ambiguity without guessing.
3. **CAMR — Capability-Aware Mission Router**: routes mission steps using capability, permission, trust, latency, reversibility, freshness, and availability without weakening constraints.
4. **DPC — Decision Patch Compressor**: reports only changed facts/recommendations/blockers/actions so users see decision deltas instead of repeated prose.
5. **RSE — Resilience Scenario Engine**: stress-tests plans against tool outage, permission loss, stale sources, and schema drift using explicit fallback contracts.

These concepts are intentionally separated from existing workstreams discovered in AI-CONTEXT, including proposal generation, human authority/agency, delegation leases, policy impact, side-effect transactions, evidence/proof labs, semantic continuity, truth surfaces, conformance/substitution, preflight, and shadow assurance.

## Cross-system pipeline
The integrated test demonstrates a single workflow across all five systems: stale evidence blocks a decision, a reversible refresh experiment is selected, a suitable capability is routed, only the resulting decision delta is surfaced, and the action plan is checked against a live-tool outage.

## Immutable rules
- Missing information never becomes a fact.
- Hard requirements are never silently relaxed to force a result.
- Identical inputs produce deterministic outputs.
- The reference implementation performs no network or repository side effects.
- Unknown or uncoverable critical conditions fail closed.
- This lab does not claim current NEXY.AI production behavior or compatibility.

## Verification
The final self-contained bundle passes:
- Python compile check
- 15 deterministic unit/integration tests
- 5,000-node UDM dependency-chain test without recursion failure
- integrated five-system workflow test

A separate local 10,000-node UDM benchmark was observed around 0.015 seconds in this runtime. That is evidence from this environment, not a production SLA.

Run:

```bash
python verify.py
```

## Future integration boundary
Use adapters from real NEXY.AI runtime records into these data types. Do not copy the lab directly into production. Revalidate against the authoritative NEXY.AI specification, connector contracts, real data volumes, and user-experience requirements before any integration.
