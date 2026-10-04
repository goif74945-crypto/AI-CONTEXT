# Temporary Execution Memory — NEXY Evolutionary Proposal Court (EPC) Lo4-20

**Operational CHAT_ID:** `CHAT-20261005-0309-NEXY-EPC-EVOLUTIONARY-PROPOSAL-COURT-20`
**Platform-native ChatGPT conversation ID:** `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
**Started:** 2026-10-05T03:09+07:00
**Execution status:** IN_PROGRESS
**Authority:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`
**Writable repository:** `goif74945-crypto/AI-CONTEXT`
**Writable namespace:** this folder plus the central `คลังข้อมูลเสริม/VOTES/` append-only vote namespace requested by the user.
**Protected scope:** every repository whose name contains `NEXY.AI` is READ-ONLY; no mutation is authorized.

## Objective
Build a deterministic, evidence-bound external proposal court for Lo4 artifacts in AI-CONTEXT. EPC may inspect, compare, defer, KEEP, CUT-as-archive/reject/supersede, and compile promotion handoff evidence. EPC must never change NEXY Core state, bypass JUDGE/verification, rewrite Canon, or auto-promote a proposal.

## Authoritative baseline observed before mutation
- Canon source: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx` content, obtained from the Drive object whose filename ends in .txt but whose bytes are Microsoft Word OOXML.
- Canon SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Canon non-empty paragraphs: 10,979.
- NEXY implementation repo: `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`, observed commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT baseline before this checkpoint: `55469befc00844f14993c98c104a29c99dff7a0b`.

## Canon constraints already verified
- Spec paragraph 176: Human layer may suggest/warn/guide attention but has no right to change Core state.
- Spec paragraphs 214-234: Core owns decision/validate/verify/User Law/freeze; Human layer cannot override or bypass verification.
- Spec paragraph 2838: AGENT propose only; SWARM debate only; VERIFY validates evidence; CORE decides. Canon writes require Core approval + verification + version bump.
- Existing NEXY code `packages/phase-f/lo2/refinement.ts` already owns experimental law-candidate lineage and promotion proof. EPC must not duplicate or replace that runtime authority.
- Existing NEXY Q64.64 overflow law is scope-bound: Core fixed128 overflow freezes; G15 simulation uses deterministic saturation. EPC will use explicit fail-closed checked Q64.64 and will not claim to define NEXY-global numeric policy.

## EPC vote law from user directive
Each CHAT_ID has at most one KEEP round and one CUT round for its lifetime.
DEFER / INSUFFICIENT_EVIDENCE / WIP are statuses, not vote rounds.
Votes are append-only evidence records. Prior votes are not rewritten.
UNKNOWN/WIP is never sufficient CUT evidence.
CUT means archive/rejected/superseded by default, never physical deletion.
No vote can override Canon/LAW/JUDGE or cause automatic NEXY promotion.

## Novelty boundary
Repository search found no exact current AI-CONTEXT hit for:
- `Evolutionary Proposal Court`
- `vote entitlement KEEP CUT`
- `candidate lineage proposal genome`
- `semantic novelty witness overlap`
- `archive rejected superseded proposal`
This proves only absence in the inspected repository search surface, not universal semantic uniqueness.

## Proposed 20-engine axis
1. EPCHASH64 — Canonical Proposal Fingerprint
2. RIGHTS64 — One-KEEP/One-CUT Entitlement Ledger
3. SNAPLOCK64 — Evaluation Snapshot Binder
4. EVIDENCE64 — Evidence Maturity Lattice
5. SEMDIFF64 — Deterministic Semantic Overlap Vector
6. DUPWIT64 — Duplication Witness Compiler
7. CANONCLASH64 — Canon Conflict Surface
8. DEPGRAPH64 — Candidate Dependency DAG Guard
9. LINEAGE64 — Immutable Candidate Lineage Validator
10. MUTDIST64 — Revision Mutation Distance Meter
11. VALUE64 — Non-compensatory Implementation Value Gate
12. VERIFYGAIN64 — Verification Value Estimator
13. SECDELTA64 — Security Impact Delta
14. DETDELTA64 — Determinism Impact Delta
15. MAINTCOST64 — Maintenance Cost Estimator
16. PORTFOLIO64 — Diversity-Preserving Active Set Selector
17. SUPERSEDE64 — Supersession Proof Compiler
18. DEFER64 — Premature-CUT Prevention Gate
19. VOTECAPSULE64 — EPC Vote Record Compiler/Validator
20. HANDOFF64 — Non-executing Promotion Handoff Capsule

## Current execution ledger
BOOT / context / actual spec hash / NEXY read-only authority inspection: PASS.
Semantic collision scan: PARTIAL, exact phrase scan PASS; broader overlap analysis in progress.
Task Contract: IN_PROGRESS.
TDD RED: NOT_RUN.
Implementation: NOT_STARTED.
E1/E2/E3: NOT_VERIFIED.
Publication of tested bytes: NOT_STARTED.
EPC KEEP entitlement: UNUSED.
EPC CUT entitlement: UNUSED.

## Resume rule
Refresh NEXY and AI-CONTEXT heads, re-read this checkpoint and Task Contract, continue from the first non-PASS gate. Never mutate a repository whose name contains NEXY.AI. Never convert Lo4/EPC output into Canon authority.
