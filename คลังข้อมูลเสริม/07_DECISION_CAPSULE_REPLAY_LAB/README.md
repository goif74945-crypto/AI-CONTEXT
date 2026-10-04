# NEXY Decision Capsule & Replay Lab

**Status:** AI PROPOSAL / REFERENCE IMPLEMENTATION / NOT CANONICAL NEXY LAW  
**Storage:** `goif74945-crypto/AI-CONTEXT`  
**Protected project:** `goif74945-crypto/NEXY.AI-` remains read-only for this work.

## Why this exists

The existing supplemental packs cover release evidence, context retrieval, agentic security, failure taxonomy, evals and a research backlog. This lab targets a different layer: **one decision/output as a deterministic, replayable, tamper-evident transaction**.

A decision capsule records the structural path from request to context, authority resolution, allow/freeze decision, optional tool side effects, verification and terminal result. The prototype refuses to treat an AI proposal as canonical NEXY law and refuses a terminal PASS when required replay invariants are not satisfied.

## Implemented v0.1 capabilities

- deterministic canonical JSON hashing;
- normalized authority fingerprints independent of authority-list order;
- SHA-256 hash chain across ordered events;
- strict event state machine;
- explicit `ALLOW` versus `FREEZE` decision boundary;
- tool intent/result pairing by `action_id` and intent digest;
- PASS requires at least one verification and all verification states PASS;
- FAIL/BLOCKED/FREEZE terminal-state proof rules;
- final output digest verification;
- structural capsule diff for authority/event/output divergence;
- payload-minimized public trust receipt;
- CLI compile/verify/replay/diff/receipt;
- stdlib-only runtime and stdlib `unittest` suite.

## Quick start

```bash
cd 07_DECISION_CAPSULE_REPLAY_LAB
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m nexy_dcr.cli compile examples/pass-plan.json examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli verify examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli replay examples/pass-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli receipt examples/pass-capsule.json
```

Freeze example:

```bash
PYTHONPATH=src python -m nexy_dcr.cli compile examples/freeze-plan.json examples/freeze-capsule.json
PYTHONPATH=src python -m nexy_dcr.cli replay examples/freeze-capsule.json
```

## Trust boundary

This implementation proves only its own capsule-format and replay invariants under the executed tests. It does **not** prove NEXY.AI currently implements this design, and it does not prove provider, runtime, deployment, security or product behavior in the separate NEXY repository.

## Research grounding

The design borrows generic provenance ideas from W3C PROV (entities/activities/agents and provenance used for trust/reproduction) and distributed tracing ideas from OpenTelemetry (immutable propagated context and stable identifiers). Those external models are inspiration, not NEXY authority.

## Core invariant

`same capsule structure -> same hashes -> same replay result`, or verification fails explicitly.

No hidden clock, randomness, network, filesystem or environment input is used in capsule identity.
