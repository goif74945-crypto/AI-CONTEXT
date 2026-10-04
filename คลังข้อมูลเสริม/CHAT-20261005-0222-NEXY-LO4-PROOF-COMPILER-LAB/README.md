# NEXY Lo4 Proof Compiler Lab

> **Status:** `Lo4_AI_PROPOSAL_ONLY`  
> **Canon authority:** none. This workspace is experimental and has no power over NEXY Canon unless formally promoted by authorized project governance.

This lab contains five deterministic reference systems designed to strengthen a future NEXY integration without modifying the NEXY.AI implementation repository.

## The five proposals

1. **Authority Provenance Seal (APS)** — proves the authority lineage of a requirement/claim and blocks authority escalation without a promotion receipt.
2. **Uncertainty Containment Lattice (UCL)** — propagates `UNKNOWN`, `NOT_VERIFIED`, `CONFLICT`, and `FAIL` only through explicit dependency edges.
3. **Minimum Proof Planner (MPP)** — selects an exact minimum-cost set of available evidence probes while preserving required evidence classes.
4. **Requirement Boundary Witness Engine (RBWE)** — compiles a small deterministic requirement DSL into positive, negative, and missing-input witnesses, and detects selected contradictions.
5. **Proof-Carrying Output Compiler (PCOC)** — releases user-visible text only when authority, epistemic state, and evidence requirements all pass; otherwise it emits a structured freeze.

## Reference flow

```text
Authority input
   ↓
APS: validate lineage / stop authority laundering
   ↓
UCL: contain epistemic blockers to affected claims
   ↓
MPP: choose the cheapest legal proof plan
   ↓
RBWE: generate boundary witnesses for executable requirements
   ↓
PCOC: compile one proven output or FREEZE
```

## Run locally

Requires only Python 3.11+ standard library.

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Integration boundary

The package intentionally has no provider API, network, database, secret, or NEXY runtime dependency. It is a reference contract/prototype. Actual integration with NEXY.AI, runtime correctness, deployment, performance, and security remain **NOT_VERIFIED** until tested against the exact authorized target implementation and environment.
