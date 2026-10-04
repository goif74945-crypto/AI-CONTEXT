# NEXY Auxiliary Verification Mesh — Mission Contract

## Classification
**AI_PROPOSED_CONCEPT / EXPERIMENTAL / OUTSIDE NEXY.AI IMPLEMENTATION REPOSITORY**

Nothing in this folder is current NEXY build law merely because it exists here.

## Objective
Design, implement, and test five standalone auxiliary systems that can integrate with NEXY.AI through explicit data contracts while preserving NEXY's evidence-first, deterministic, fail-closed principles.

## In scope
- New files only under this mission root in AI-CONTEXT.
- Five independent concepts plus one integration adapter.
- Python 3 standard-library implementation with deterministic serialization.
- Unit and integration tests.
- Design, code, tests, evidence, and resumable state.

## Protected scope
- No mutation to any repository whose name contains `NEXY.AI`.
- No mutation outside this mission root.
- No reinterpretation of an AI-proposed concept as canonical NEXY law.
- No secrets, credentials, or hidden chain-of-thought.

## Source facts used
- `projects/NEXY.AI/overview.md`: NEXY is a deterministic AI control hub; one legal verified output or freeze/silence.
- `projects/NEXY.AI/deep/doc-c-vnext-build-spec.md`: current vNEXT includes evidence, release gates, explicit FSM states, provider-independent AgentAdapter, LAW/JUDGE/VAULT boundaries.
- `projects/NEXY.AI/deep/capability-registry-chaos.md`: future source-design already contains a constitutional capability registry/admission stack. Concept 4 here is intentionally scoped to runtime provider/tool admission, not a replacement for G20/G21.
- `rules/VERIFICATION.md`: evidence classes E0-E7 and no evidence-class substitution.
- `AI-EXECUTION-KERNEL.md`: evidence before status, scope control, streaming checkpoints.

## Acceptance criteria
1. Exactly five named concepts are present and clearly marked AI-proposed.
2. Each concept has DESIGN.md, implementation code, executed tests, and EVIDENCE.md.
3. An integration adapter demonstrates how the concepts can compose without importing NEXY.AI code.
4. Tests cover positive and negative/freeze paths.
5. Deterministic outputs are stable under semantically equivalent input ordering where intended.
6. No external runtime dependency is required beyond Python 3 standard library.
7. No protected repository/path is mutated.
8. Completion claims are backed by fresh executed evidence.

## Planned build order
C1 Proof Lattice → C2 Authority Compiler → C3 Replay Seal → C4 Runtime Capability Gate → C5 Delta Impact → integration → regression audit.
