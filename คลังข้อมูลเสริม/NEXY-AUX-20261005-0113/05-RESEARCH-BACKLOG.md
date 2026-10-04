# NEXY Auxiliary Research Backlog
Status: RESEARCH QUESTIONS / NOT REQUIREMENTS

This backlog intentionally contains UNKNOWN/HYPOTHESIS items. Completion requires evidence, not prose.

## R1 — Proof lineage soundness
Question: Can evidence invalidation be dependency-sliced without allowing stale PASS leakage?
Method: build formal dependency examples + mutation corpus + property tests.
Success: no relevant mutation retains invalid proof; irrelevant mutation avoids unnecessary invalidation.
Failure: any stale PASS survives.

## R2 — Determinism envelope
Question: Which NEXY subsystems require strict determinism vs controlled nondeterminism?
Need: explicit ontology for pure core, orchestration, provider calls, UI, runtime, deployment.
Risk: calling the whole product “deterministic” can blur nondeterministic external boundaries.

## R3 — Authority conflict algebra
Question: Can authority resolution be represented as a deterministic partial order with explicit incomparable states?
Need: rules for temporal supersession, domain-specific authority and evidence applicability.
Output: conflict resolver spec + counterexample suite.

## R4 — Freeze composability
Question: How should local freezes compose across task/session/project/deployment without unnecessary global halt?
Test: concurrent independent tasks + shared dependency failures + security incidents.

## R5 — Capability drift
Question: How to detect a tool/model that keeps the same interface but changes behavior?
Potential evidence: behavioral canaries, digest/version, policy probes, provider metadata.
Warning: behavior fingerprint is heuristic, not authority.

## R6 — Prompt-injection containment
Research trust-boundary design for tool outputs, web content, documents, agent messages and memory.
Acceptance must include executed adversarial tests if ever implemented.

## R7 — Memory poisoning resistance
Question: How does VAULT distinguish verified durable truth from persuasive but unverified generated content?
Explore staged memory states, provenance, promotion gates, revocation/invalidation.

## R8 — Idempotent side effects
Model exact-once illusion vs at-least-once reality for external APIs.
Need request identity, dedup ledger, commit/ack ambiguity handling, reconciliation.

## R9 — Long-running workflow recovery
Design crash-consistent resumability:
checkpoint identity, replay safety, leased work, orphan detection, partial side effects, compensation.

## R10 — Multi-agent consensus fallacy
Test scenarios where many agents agree on the same wrong claim due to correlated training/context.
Goal: demonstrate why consensus cannot replace independent evidence.

## R11 — Evidence artifact integrity
Explore content-addressing, signatures/seals, provenance manifests, environment binding, retention and tamper evidence.

## R12 — Policy evolution
How should old evidence be treated after LAW/policy version changes?
Need backward applicability rules and explicit re-verification triggers.

## R13 — Secret minimization
Map where credentials may appear across agents/tools/logs/evidence. Design redaction + least-authority handling without destroying useful provenance.

## R14 — Observability without authority leakage
Telemetry should explain behavior without becoming a backdoor control plane.
Test whether logs/metrics can accidentally influence deterministic decisions.

## R15 — Safe degraded modes
Define which features may degrade while preserving NEXY invariants and which must freeze.
No silent semantic downgrade.

## R16 — External provider epistemics
Provider “success” may not prove intended side effect.
Research confirmation patterns: read-after-write, signed receipts, idempotency keys, reconciliation.

## R17 — Schema evolution
Design compatibility law for persisted Vault objects, evidence records, capability manifests and task contracts.

## R18 — Supply-chain admission
Map dependency/plugin/model/container provenance to capability admission and release proof.

## R19 — Deployment identity
Define exact mapping source commit → lockfiles → build inputs → image digest → config fingerprint → deployment instance → E6 evidence.

## R20 — Physical/robotics safety boundary
Keep AI orchestration separate from independent safety mechanisms. Any physical safety claim requires E7/HIL/physical evidence; design prose cannot promote it.

## Prioritization suggestion (AI proposal)
P0 integrity: R1,R3,R6,R7,R8,R11,R19.
P1 resilience: R4,R9,R12,R15,R17.
P2 ecosystem: R5,R13,R16,R18.
P3 advanced: R2,R10,R14,R20.

## Research record template
ID; question; authority relevance; source plan; hypothesis; experiment; evidence class; result; contradictions; limitations; promotion decision.
