# Temporary / Resumable Execution Memory

Status: IMPLEMENTATION_VERIFIED / STORAGE_COMMIT_IN_PROGRESS
Chat reference: CHAT-20261005-0142-NEXY-EVIDENCE-INDEPENDENCE-KERNEL

## Objective
Create a novel additive system useful to NEXY.AI without mutating any NEXY.AI repository. Design it, implement it, attack it with negative-path tests, repair defects, re-test, and preserve design + code + tests + evidence together in AI-CONTEXT.

## Gap selected
Existing AI-CONTEXT material discusses correlated-consensus laundering and states that multiple agents sharing the same source are one correlated lineage, not multiple independent confirmations. Direct inspection found that rule in advisory/backlog form. The inspected ProofGraph workspace contained only .gitignore, and the inspected Evidence Capsule workspace contained only its session-memory file. No executable evidence-independence kernel was established by those inspected surfaces.

## Scope lock
IN SCOPE:
- deterministic evidence-independence analyzer;
- strict JSON contract;
- dependency DAG and ancestry lineage closure;
- exact maximum pairwise-independent witness solver;
- intrinsic duplicate-artifact correlation;
- stale revision, evidence-class, blindness, self-verification and contradiction gates;
- deterministic search budget;
- adversarial, CLI and exhaustive solver tests;
- integration proposal and future research ideas.

OUT OF SCOPE:
- editing NEXY.AI source;
- production integration or deployment;
- claiming underlying evidence is truthful;
- cryptographic attestation of lineage metadata;
- replacing NEXY LAW or JUDGE.

## Protected scope
All repositories whose name contains NEXY.AI are mutation-forbidden in this task.

## Failure / repair history
1. Initial reference tests passed.
2. Design re-audit found two hazards not yet guarded: empty configured lineage could be treated as independent, and exact witness search lacked an explicit work budget.
3. The contract and solver were hardened.
4. A test fixture then failed because producer_lineage no longer contained producer_id. The fixture was corrected rather than weakening the invariant.
5. Bundled implementation passed 24/24 tests.
6. During ad-hoc final validation, two harness mistakes were exposed and corrected: one used schema instead of schema_version; another read a wrong result-key name. These were harness defects and are preserved rather than hidden.

## Verified local state before storage commit
- compileall: PASS.
- JSON spec syntax parse: PASS.
- unit/adversarial/exhaustive suite: 24/24 PASS.
- exhaustive exact-solver oracle: all simple graph topologies through 5 vertices PASS against brute force.
- deterministic CLI replay: 25/25 byte-identical outputs.
- bounded stress: 16, 24, 32, 48, 64 evidence-node cases completed under the configured 1,000,000-state budget.
- core imports: Python standard library only.

## Resume law
Before changing semantics, rerun the full test suite and exact solver oracle. Any NEXY.AI integration requires separate explicit authorization.