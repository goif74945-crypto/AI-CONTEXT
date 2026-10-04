# NEXY Change Impact Graph Engine Lab (CIGE)

Status: REFERENCE IMPLEMENTATION / ADVISORY / NOT INTEGRATED INTO NEXY.AI
Created: 2026-10-05T01:37+07:00
Storage target: `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/`
Protected target: every repository whose name contains `NEXY.AI` remains read-only for this task.

## Why this exists
NEXY's current context separates design, implementation, runtime, and deployment evidence, and requires exact revalidation after relevant change. CIGE is an additive reference engine for answering a narrower question deterministically:

> Given a declared dependency/verification graph and a set of changed nodes, which downstream contracts, modules, artifacts, tests, and evidence are impacted and must be revalidated?

It is designed to reduce two common failure classes:
1. stale evidence surviving after a dependency changes;
2. regression scope being chosen by intuition instead of an explicit graph.

## Authority classification
- FACT_PROJECT: NEXY current context requires explicit dependency/test impact review for out-of-scope extensions and distinguishes evidence from implementation truth.
- FACT_PROJECT: NEXY build-spec context defines deterministic/freeze behavior, explicit validation boundaries, dependency rules, and test gates.
- PROPOSAL_AI: CIGE itself, its graph schema, algorithms, reason codes, and adapter strategy are proposed by AI. They are **not** current NEXY requirements unless explicitly promoted by user/project authority.
- NOT_VERIFIED: No runtime integration with the NEXY.AI implementation repository was performed because writes to that repository are forbidden in this task.

## Core properties
- deterministic canonicalization and SHA-256 graph/change-set digests;
- pure core API with no clock, RNG, network, filesystem, environment, or process reads;
- unknown changed nodes FREEZE rather than being dropped;
- schema/reference errors FREEZE;
- hard dependency cycles FREEZE;
- traversal is bounded and FREEZEs on limit rather than returning a silently truncated answer;
- causal paths explain why each node is impacted;
- tests/evidence in the impact closure become `required_revalidation`;
- critical changed nodes without any reachable test/evidence coverage FREEZE with `EVIDENCE_MISSING`;
- canonical sorting makes result independent of source node/edge order.

## Files
- `src/impact_graph.mjs` — deterministic core.
- `src/cli.mjs` — non-authoritative file I/O shell for local use.
- `fixtures/nexy.sample.json` — small illustrative graph using current NEXY concept names; it is not a complete NEXY graph.
- `tests/impact_graph.test.mjs` — unit/regression suite.
- `DESIGN.md` — architecture and failure model.
- `INTEGRATION_CONTRACT.md` — proposed safe boundary for future NEXY integration.
- `REQUIREMENT_LEDGER.md` — requirements → implementation → evidence mapping.
- `PROPOSALS.md` — future ideas explicitly labeled proposals.
- `evidence/TEST-EVIDENCE.md` — executed proof record.
- `00_EXECUTION_STATE.md` — resumable execution checkpoint.

## Run locally
```bash
npm test
npm run demo
```

## Non-goals
- It does not read or mutate the NEXY.AI repository.
- It does not claim to reconstruct the full 837-row NEXY source matrix.
- It does not replace DOC-B/DOC-C/DOC-E authority.
- It does not prove production integration, deployment readiness, or runtime correctness of NEXY.AI.
- It does not auto-edit impacted files or auto-approve releases.

## Integration posture
The core accepts plain JSON-compatible structures and returns plain JSON-compatible structures. This is intentional: a future NEXY adapter can validate a trusted graph snapshot, call the core, bind its digests to a revision/trace/evidence record, and either schedule the returned validation frontier or FREEZE. The adapter must remain the authority boundary; CIGE is analysis, not authority.
