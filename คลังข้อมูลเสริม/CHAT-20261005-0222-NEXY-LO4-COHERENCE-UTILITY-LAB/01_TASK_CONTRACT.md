# Task Contract

## Objective
Create a self-contained five-system Lo4 experimental lab under AI-CONTEXT supplemental knowledge. Every system must have an explicit purpose, invariants, fail-closed behavior, executable reference code, negative tests, and a proposed NEXY adapter boundary.

## Target
`คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-LO4-COHERENCE-UTILITY-LAB/` on `goif74945-crypto/AI-CONTEXT` default branch.

## Authorized scope
- create files only under the target folder;
- run authored code/tests in an isolated local runtime;
- read AI-CONTEXT and read-only NEXY context needed for compatibility reasoning;
- persist design, code, tests, evidence, defect history, hashes, and temporary memory.

## Protected scope
- all repositories whose names contain `NEXY.AI`;
- existing AI-CONTEXT files outside the target folder;
- secrets/credentials/private user data;
- Canon/project requirements not explicitly promoted by authorized sources.

## Immutable requirements
1. Lo4 outputs remain advisory/experimental until formal promotion.
2. Same semantically equivalent input must produce deterministic output where order is declared irrelevant.
3. Malformed identity-sensitive or ambiguity-sensitive input fails explicitly.
4. No hidden fallback from UNKNOWN/CONFLICT/FREEZE to PASS.
5. Design, code presence, local runtime evidence, NEXY integration, and deployment remain separate status classes.
6. Each concept must solve a materially different problem from the inspected sibling labs.
7. Reference code uses only the Python standard library and performs no network/model/subprocess/credential access.
8. Cross-module integration must demonstrate composition without granting authority.

## Concepts
- **BKR:** bitemporal valid-time/known-time reconstruction with late-arrival and correction semantics.
- **CEML:** commutative/idempotent merge of concurrent claim replicas while preserving unresolved conflicts.
- **CUVL:** causal chain from proposal mechanism to user outcome, metric, guard metric, falsifier, and evidence readiness.
- **STCE:** scoped terminology definitions/aliases with overlap ambiguity and alias-cycle rejection.
- **FSA:** compositional result algebra over PASS/FAIL/FREEZE/UNKNOWN/CONFLICT/NOT_VERIFIED with explicit dependency policy.

## Required evidence
- E0: all intended files present and remote read-back succeeds.
- E1: `python -m compileall -q .`.
- E2: focused unit/adversarial tests for every concept.
- E3-local: integration test across all five concepts.
- Identity: SHA-256 manifest of tested source/tests and remote read-back equality for critical files.

## Stop conditions
Freeze rather than guess if a required step would mutate NEXY.AI, overwrite another chat folder, silently promote proposal to Canon, require unavailable authority, or prevent exact tested-source verification.

## Deliverables
- 00_TEMP_MEMORY.md
- 01_TASK_CONTRACT.md
- README.md
- DESIGN.md
- NOVELTY_MATRIX.md
- TEST_MATRIX.md
- src/*.py
- tests/test_*.py
- tests/test_integration.py
- evidence/*
- SHA256SUMS.txt
- DEFECT_LOG.md
- FINAL_AUDIT.md
