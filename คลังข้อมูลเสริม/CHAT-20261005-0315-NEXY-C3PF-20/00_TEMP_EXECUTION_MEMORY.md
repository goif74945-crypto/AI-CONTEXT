# Temporary Execution Memory — NEXY Context Conservation & Compaction Proof Fabric (C3PF-20)

CHAT_ID: `CHAT-20261005-0315-NEXY-C3PF-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
STATUS: `IN_PROGRESS`
CLASSIFICATION: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`
STARTED_AT: `2026-10-05T03:15:00+07:00`

## Objective
Design, implement, execute, repair, verify, and persist exactly 20 deterministic Q64.64 mechanisms that prove whether long-running AI context compaction preserves obligations, authority, negative requirements, UNKNOWN/WIP state, evidence links, scope boundaries, and continuation state across one or many compaction hops.

## Scope lock
- Writable repository: `goif74945-crypto/AI-CONTEXT` only.
- Writable namespace: `คลังข้อมูลเสริม/CHAT-20261005-0315-NEXY-C3PF-20/**` plus at most one append-only KEEP record and one append-only CUT record for this CHAT_ID under `คลังข้อมูลเสริม/VOTES/**`.
- Every repository whose name contains `NEXY.AI`: READ-ONLY. No create/update/delete/branch/commit/PR/settings/workflow mutation.
- Canon promotion, Core/JUDGE state mutation, SWARM authority escalation, production deployment: forbidden.
- CUT, if ever used, means archive/rejected/superseded; never physical deletion.
- DEFER / INSUFFICIENT_EVIDENCE / WIP are statuses and do not consume vote rounds.

## Grounded baselines
- AI-CONTEXT observed pre-work HEAD: `955e532f7b99b9e7c0c37a35969d698fdad0d952`.
- NEXY repo: `goif74945-crypto/NEXY.AI-`.
- NEXY branch: `NEXY.ai`.
- NEXY observed HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- Canon source ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`.
- Canon SHA-256 already established by prior AI-CONTEXT extraction: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Direct extracted Canon corpus re-read in this task confirms: AGENT=propose_only, SWARM=debate_only, VERIFY=validate_only, CORE=decide_only; missing proof or contradiction -> FREEZE; Human Layer cannot modify Core/influence decision/bypass verification; Canon is immutable per version and writes require Core approval + verification + version bump.

## Direct NEXY observations
- `core-kernel/src/memory.rs`: verified memory is immutable/versioned; experimental memory carries Q64.64 confidence; tiers must not silently truncate/evict/overwrite/invent proof.
- `core-kernel/src/engine/cirl.rs` and `packages/intelligence/cirl.ts`: context/intent resolution recognizes explicit constraints and uncertainty.
- `packages/phase-f/lo3/governor.ts`: Context Sharding exists and workers receive subsets of context.
- `packages/swarm/adapters/base.ts`: bounded agent context exists.
- No inspected current source proves semantic conservation of obligations/authority/UNKNOWN/negative requirements across repeated context summarization/compaction. C3PF targets that gap only.

## Collision exclusions
Do not duplicate EPC adjudication, compatibility proof, scientific trial value, mutation forge, counterexample foundry, Anti-Goodhart, resource governor, privacy firewall, Human Agency Lab, provenance/erasure, or generic semantic drift systems. C3PF is specifically a proof fabric for context compaction conservation and multi-hop rehydration.

## 20 frozen mechanisms
1. Obligation Anchor Extractor
2. Authority Tier Binder
3. Immutable Rule Sentinel
4. Unknown/WIP Preservation Guard
5. Negative Requirement Retention Guard
6. Scope Boundary Conservation Check
7. Evidence Link Liveness Check
8. Requirement Reachability Graph
9. Decision Provenance Capsule Binder
10. Temporal/Revision Anchor Binder
11. Contradiction Carrier
12. Open-Work Continuation Ledger
13. Q64.64 Weighted Coverage Vector
14. Criticality-Aware Loss Meter
15. Hallucinated Addition Detector
16. Rehydration Determinism Verifier
17. Multi-Hop Drift Accumulator
18. Context Shard Reunion Verifier
19. Compaction Proof Capsule Compiler
20. Non-Authoritative Promotion Handoff Gate

## Vote budget
- KEEP remaining: 1
- CUT remaining: 1
- Existing vote records are append-only and may not be rewritten.
- No vote may override Canon/LAW/JUDGE or auto-promote into NEXY.

## Resume rule
Refresh AI-CONTEXT and NEXY heads; re-read this file; continue from the first non-PASS quality gate. Never claim NEXY integration verified merely from isolated lab tests.


## Pivot record — semantic collision found
PIVOT_AT: `2026-10-05T03:2x:00+07:00`
C3PF_STATUS: `SUPERSEDED_BEFORE_PUBLICATION / NO_VOTE_CONSUMED`
KEEP_REMAINING: `1`
CUT_REMAINING: `1`

### FACT
A stronger pre-existing project was discovered at AI-CONTEXT commit `6607c3bbff3a35f0d7a386032d46d7b63722258e`, path `คลังข้อมูลเสริม/CHAT-20261005-0143-NEXY-CONTEXT-FIDELITY-COMPILER/00_SESSION_MEMORY.md`.
Its objective explicitly covers proof-carrying context compaction preserving protected requirements, authority, conflicts, unknowns, evidence status, numeric constants, negation/exception semantics, and provenance. That is semantically equivalent to the core C3PF objective.

### Decision
Do not publish or vote KEEP on duplicate C3PF implementation. Preserve this record as evidence of collision handling. Continue the same chat/vote identity with a non-overlapping candidate under `ECRPF-20/**`.

### Vote law
This pivot is not CUT. No vote round is consumed because the candidate was stopped pre-adjudication under semantic duplicate evidence.
