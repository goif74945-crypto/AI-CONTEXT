# EPC Lo4 Frontier 20 — Temporary Execution Memory

CHAT_ID: `CHAT-20261005-0310-NEXY-EPC-LO4-FRONTIER-20`

> This is a project-scoped execution identifier created for EPC lineage. It is not claimed to be an internal ChatGPT platform conversation ID.

## Authority baseline

- User objective: build a large, useful Lo4 innovation project for NEXY.AI without modifying `goif74945-crypto/NEXY.AI-`.
- Writable target: `goif74945-crypto/AI-CONTEXT`, branch `main`, under `คลังข้อมูลเสริม/` only.
- Protected target: `goif74945-crypto/NEXY.AI-` is READ-ONLY for this task.
- NEXY branch observed: `NEXY.ai`.
- NEXY commit baseline inspected: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT baseline inspected before mutation: `55469befc00844f14993c98c104a29c99dff7a0b`.
- Canonical NEXY-IGNIS SHA-256 from AI-CONTEXT provenance: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Current source-normalization denominator: 837 normalized requirement rows. The historical 215 registry is deprecated and is not used as authority.

## Current design

System name: **NEXY Evolutionary Proposal Court (EPC) — Lo4 Frontier 20**.

Classification: `LO4_AI_PROPOSAL_ONLY_NON_AUTHORITATIVE`.

Purpose: evaluate AI-proposed supplemental systems under deterministic Q64.64 scoring and evidence gates while preserving Canon/Core/JUDGE authority. EPC can recommend, defer, freeze, or identify a CUT candidate, but cannot promote Canon, mutate Core state, inject canonical transitions, or write NEXY.AI.

20 implemented engines: E01..E20. See `03_CONCEPTS_20.md`.

## Execution history

1. Read AI-CONTEXT bootstrap/execution/routing/security/verification law.
2. Read current NEXY project overview, deep index and normalized build matrix.
3. Inspected NEXY code read-only at commit `9e615b...`, including Core Q64.64 `Fixed128` and Lo3 Q64 usage.
4. Inspected existing supplemental systems including Proposal Forge, Evolution Atlas, and Anti-Goodhart Q64 pack.
5. Searched AI-CONTEXT for `Evolutionary Proposal Court`, `EPC`, `VOTE_ID`, `KEEP ROUND`, and `CUT ROUND`; no matching implementation was found in the observed default-branch code search.
6. Implemented TypeScript EPC with Node built-ins only and no runtime dependencies.
7. First test run: **39/40 PASS, 1 FAIL**. Defect: E07 detected a dependency cycle as hard-block but final recommendation omitted E07 from the hard-block aggregation list.
8. Root cause fixed by adding E07 to the non-compensatory hard-block set.
9. Regression run: **40/40 PASS**.

## Non-negotiable EPC voting law

- One CHAT_ID may consume KEEP exactly once and CUT exactly once.
- DEFER / INSUFFICIENT_EVIDENCE / WIP do not consume either vote round.
- A previous vote is immutable. A revision/evidence addendum does not create a new voting right.
- UNKNOWN/WIP cannot be used as a CUT ground.
- CUT requires evidence-backed semantic grounds; naming similarity alone is insufficient.
- CUT means archive/rejected/superseded by default, not physical deletion.
- A vote cannot override Canon/Law/JUDGE or automatically promote anything into NEXY.AI.

## Pending before publication

- Produce final architecture, threat model, novelty audit, integration contract, requirement ledger, and exact test/evidence artifacts.
- Publish project only inside `คลังข้อมูลเสริม/CHAT-20261005-0310-NEXY-EPC-LO4-FRONTIER-20/`.
- Re-anchor final evidence to the exact AI-CONTEXT commit containing the implementation.
- Emit at most the KEEP round after exact-head verification; reserve CUT unless independently justified.

## Pre-publication concurrent refresh

AI-CONTEXT moved after the original baseline. A new adjacent project `CHAT-20261005-0316-GPT56SOL-EPC-CEGAR20` appeared. Its objective is Abstract Interpretation + CEGAR proof compilation, not proposal-round governance. Collision was re-audited and documented in `04_NOVELTY_COLLISION_AUDIT.md`; no semantic reason to discard this project was found, but global superiority remains NOT_VERIFIED.
