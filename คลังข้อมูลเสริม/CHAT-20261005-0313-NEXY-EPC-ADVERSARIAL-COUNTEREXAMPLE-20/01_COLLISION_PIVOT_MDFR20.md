# COLLISION-DRIVEN PIVOT — 2026-10-05

CHAT_ID: CHAT-20261005-0313-NEXY-EPC-ADVERSARIAL-COUNTEREXAMPLE-20
STATUS: IN_PROGRESS
DECISION: PIVOT_BEFORE_CODE_PUBLICATION

## Newly observed concurrent work
After the initial local prototype was implemented and tested, current AI-CONTEXT was refreshed. The refresh exposed two materially adjacent projects that were not present at the earlier collision snapshot:

1. CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20
   - injects known-invalid verification/policy mutants;
   - measures whether independent sentinels kill those mutants;
   - overlaps materially with generic authority/evidence/Q64/canonicalization attack families.

2. CHAT-20261005-0316-GPT56SOL-EPC-CEGAR20
   - abstract interpretation + counterexample-guided abstraction refinement;
   - generates abstract counterexamples, validates concrete witnesses, and refines abstractions.

## Consequence
The initial **generic Adversarial Counterexample Reactor** implementation is NOT published as the final candidate because its generic attack surface would overlap semantically with these projects.

The prior local tests remain development evidence only and do not become a promotion/novelty claim.

## New locked surface
The final candidate is narrowed to:

**NEXY EPC Metamorphic Differential Falsification Reactor 20 (MDFR20)**

It is specifically a black-box / observation-driven verification layer for declared semantic equivalences and independent implementation differentials. It does NOT:
- mutate source to create mutants;
- evaluate mutation-testing adequacy;
- perform abstract interpretation;
- implement CEGAR;
- plan integration ecology;
- own vote rights or Court adjudication;
- perform phase-boundary analysis.

## Final 20 mechanisms
01 SECB — Semantic Equivalence Contract Binder
02 KOIP — Key-Order Invariance Probe
03 SPIP — Set-Permutation Invariance Probe
04 RIP — Replay Idempotence Probe
05 DNP — Duplicate-Neutrality Probe
06 IMIP — Irrelevant-Metadata Invariance Probe
07 SRTP — Serialization Round-Trip Probe
08 DREP — Decompose-Recompose Equivalence Probe
09 EMP — Evidence-Monotonicity Probe
10 CNP — Constraint-Nonexpansion Probe
11 UCM — Uncertainty Conservation Metamorph
12 PADM — Provider Adjudication Differential Mesh
13 RDM — Runtime Differential Mesh
14 CSDM — Canonical Serializer Differential Mesh
15 ESDM — Error Semantics Differential Mesh
16 STDM — State Trace Differential Mesh
17 QXDM — Q64 Cross-Implementation Differential Mesh
18 CMR — Counterexample Minimality Reducer
19 RWCC — Replay Witness Capsule Compiler
20 MFQG — Metamorphic Falsification Qualification Gate

## Numeric / authority law
- All quantitative decision values remain checked signed Q64.64 in signed-i128 raw bounds.
- Binary floating point is forbidden from authoritative MDFR decisions.
- MDFR outputs evidence only.
- WIP is forced to DEFER.
- No MDFR output may promote Canon, mutate CORE/JUDGE/LAW, spend an EPC vote, or physically delete a candidate.

## Direct spec evidence added before final implementation
Direct source extract read:
- path: REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt
- Git blob SHA: 30b0c179670a836af61923b4b85ae89f3a40d8dc
- canonical source SHA-256 recorded by AI-CONTEXT: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Observed source law includes:
- Human Layer may suggest/warn/guide attention but may not change Core state.
- Human Layer may not override decisions or bypass verification.
- Experimental outputs require verification before durable commitment.
- NEXY uses adversarial/cross-verification before trusted release.

## Vote state
KEEP: unspent
CUT: unspent
DEFER/WIP: non-consuming

No vote is cast by this checkpoint.
