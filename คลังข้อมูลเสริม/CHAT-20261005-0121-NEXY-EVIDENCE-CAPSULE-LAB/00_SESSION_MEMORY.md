# Temporary Execution Memory — NEXY Evidence Capsule & Selective Disclosure Lab

status: IN_PROGRESS
truth_class: REPO_FACT_FOR_THIS_TASK_RECORD
durable_chat_code: CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB
platform_native_chat_id: UNKNOWN_NOT_EXPOSED
started_local: 2026-10-05T01:21:00+07:00

## Objective
Create a distinct supplemental R&D project for NEXY inside AI-CONTEXT only. The project explores privacy-preserving, tamper-evident evidence capsules that can disclose only authorized evidence fields while preserving verifiable integrity, freshness, provenance, and explicit failure semantics.

## Authority and source facts
- AI-CONTEXT Execution Kernel, Security, Verification, System Design, Implementation and Memory Update workflows govern this task.
- Current NEXY source normalization uses 837 normalized requirement rows; that matrix is source normalization, not implementation proof.
- DOC-C is current build authority; this lab does not promote itself into DOC-C.
- DOC-C states that redaction may operate on derived/copied views but must not rewrite original audit lineage; hashes remain for integrity evidence.
- NEXY design separates design, implementation, runtime, and deployment evidence.

## Why this lab is distinct
Recent sibling work already covers proof-carrying execution, evidence graphs, verification economy, reliability budgets, capability admission, idempotency/replay, compatibility evolution, experience compilation, and human-authority interaction integrity.

This lab intentionally targets a separate axis:
- field-level selective disclosure;
- redacted derived views without rewriting lineage;
- tamper-evident Merkle commitments;
- freshness and replay rejection;
- role-scoped disclosure policy;
- provenance-preserving verification bundles;
- explicit distinction between integrity and issuer authenticity.

Repository/commit keyword checks found no recent commits titled around privacy, redaction, selective disclosure, Merkle commitments, or evidence capsules.

## Truth labels
- SOURCE_FACT: grounded in canonical AI-CONTEXT/NEXY context.
- AI_PROPOSED_CONCEPT: newly designed mechanism in this lab.
- HYPOTHESIS: benefit expected but requiring future integration/runtime experiments.
- REFERENCE_IMPLEMENTATION: standalone code in AI-CONTEXT, not NEXY production code.
- NOT_VERIFIED_NEXY_RUNTIME: no claim about NEXY.AI runtime behavior.

## Authorized mutation scope
Only:
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB/`

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Existing files outside this new supplemental folder.
- Canonical 837-row matrix and NEXY project law/spec.
- Repository settings, workflows, branches, issues, and PRs unless separately authorized.
- Secrets and real credentials.

## Planned deliverables
1. task contract
2. concept/non-goals
3. architecture
4. threat model
5. protocol specification
6. requirement ledger
7. integration proposal
8. standard-library Python reference implementation
9. adversarial fixture corpus
10. unit/adversarial tests
11. package validator
12. verification report
13. final audit
14. research/adoption backlog
15. content manifest

## Verification target
- E0: every committed path can be re-fetched.
- E1: Python compile/static/package checks and JSON validation.
- E2: executed unit/adversarial tests against the exact reference source content.
- No E3/E4/E5/E6 claim about NEXY.AI.

## Stop conditions
- Any write would touch a NEXY.AI-named repository.
- Any existing sibling artifact would need destructive overwrite.
- A material authority conflict invalidates the concept.
- A real secret/credential would be persisted.
- Required write precondition cannot be established safely.

## Resume instruction
Read this file first. Then read `01_TASK_CONTRACT.md`, `03_ARCHITECTURE.md`, `05_PROTOCOL_SPEC.md`, and `09_VALIDATION_REPORT.md` when present. Do not infer PASS from file presence.
