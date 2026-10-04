# NEXY.AI Formal Assurance & Deterministic Verification Lab

Status: ACTIVE / ADVISORY / ADDITIVE-ONLY
Execution ref: NEXY-FAL-20261005-0111-ICT

## Mission
Develop reusable verification theory and machine-checkable contracts that can help future NEXY work answer four hard questions:

1. Which authority uniquely governs a decision?
2. What exact evidence is sufficient for a claim?
3. Which changes invalidate previously valid proof?
4. When must the system FREEZE instead of selecting an output?

This directory is intentionally different from the existing evidence/context/security/eval packs. It focuses on formalizable semantics and counterexample-driven verification.

## Non-authority warning
Nothing here becomes NEXY.AI law merely by existing here. Project law/spec/source/runtime evidence outrank this lab.

## Planned artifacts
- 01_AUTHORITY_CALCULUS.md
- 02_FORMAL_STATE_MODEL.md
- 03_SEMANTIC_REQUIREMENT_DIFF.md
- 04_PROOF_INVALIDATION_ALGEBRA.md
- 05_DETERMINISTIC_REPLAY_PROTOCOL.md
- 06_METAMORPHIC_CONFORMANCE.md
- 07_COUNTEREXAMPLE_CORPUS.md
- 08_MODEL_CHECKING_PLAN.md
- 09_TRACEABILITY_GRAPH.md
- 10_ACCEPTANCE_GATES.md
- INDEX.md

## Grounding
FACT_PROJECT:
- NEXY is defined as deterministic AI control / authority system.
- Stable release behavior is one legal verified output or freeze/silence.
- Current source normalization has 837 requirement rows with explicit authority/scope classes.
- Design, implementation, runtime, and deployment evidence are separate truth domains.
- PASS must match the evidence class required by the claim.

## Research law
Every proposal must state:
- inputs;
- authority assumptions;
- invariants;
- failure semantics;
- falsification method;
- evidence needed;
- known limits.

No hidden chain-of-thought is required or stored. Only inspectable contracts and conclusions are persisted.
