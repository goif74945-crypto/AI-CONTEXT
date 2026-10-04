# Closed Execution Memory — NEXY Evidence Capsule & Selective Disclosure Lab

status: COMPLETE_REFERENCE_LAB
truth_class: REPO_FACT_FOR_THIS_TASK_RECORD
durable_chat_code: CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB
platform_native_chat_id: UNKNOWN_NOT_EXPOSED
started_local: 2026-10-05T01:21:00+07:00
target_repository: goif74945-crypto/AI-CONTEXT
target_branch: main
authorized_write_scope: คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB/

## Objective completed
Designed, implemented, tested and documented a distinct AI-proposed evidence-capsule/selective-disclosure mechanism useful to future NEXY research without modifying any repository whose name contains NEXY.AI.

## Canonical context used
AI-CONTEXT bootstrap/index/execution kernel/work router; global/security/verification rules; project-start/research/system-design/artifact/implementation/verification/memory workflows; NEXY overview/deep indexes/constitutional/build-spec context; current 837-row normalized requirement matrix.

## Source-grounded motivation
NEXY separates source/design/implementation/runtime/deployment truth and DOC-C context permits redaction on derived/copied views without rewriting original audit lineage, with hashes retained for integrity. This lab explores a possible derived-view proof mechanism. It does not change DOC-C.

## Distinctness check
Concurrent/sibling work already covered experience compilation, human-authority integrity, proof/evidence infrastructure, verification economy, reliability budgets, compatibility, anti-entropy, replay/idempotency and resource governance. Repository/commit searches did not show a recent dedicated selective-disclosure/Merkle evidence-capsule lab before this task.

## Deliverables
- README.md
- design/01_TASK_CONTRACT.md
- design/02_ARCHITECTURE_PROTOCOL.md
- design/03_THREAT_MODEL.md
- design/04_REQUIREMENT_LEDGER.md
- design/05_INTEGRATION_PROPOSAL.md
- reference/reference_impl.py
- reference/test_reference_impl.py
- fixtures/adversarial-vectors.json
- schema/protocol.schema.json
- validation/06_TEST_EVIDENCE.md
- validation/07_RESEARCH_BACKLOG.md
- 10_FINAL_AUDIT.md

## Verification
E0: core package paths re-fetched from GitHub main.
E1: Python compile PASS; protocol JSON parse PASS.
E2: compact committed reference test suite 20/20 PASS.
Byte linkage:
- implementation Git blob: 6b7a899d1f65b89fd0ded881f105b843ef60e187
- tests Git blob: 0b0401e592ebc1420e88fd4e53e5c3ab4f397630
Both matched local git hash-object results before commit and GitHub create_blob results.
Core package commit: 036f3b56d23e636db155742eb64efefd8dab7de4

A larger exploratory development package reached 32/32 tests locally. Completion claims are based on the compact committed 20/20 suite because its exact bytes are linked to repository blobs.

## Concurrency/recovery record
Concurrent writes caused expected GitHub 409/422 conflicts. No force push was used. The task refreshed HEAD and retried fast-forward-only until successful.

## Known limitations
- HMAC-SHA256 is REFERENCE-ONLY, not production issuer authentication.
- no E3/E4/E5/E6 NEXY evidence;
- no asymmetric key lifecycle/revocation;
- no durable distributed replay service;
- no cross-language canonicalization proof;
- no zero-knowledge privacy;
- no real NEXY RBAC/Vault/Audit integration.

## Resume / adoption rule
Read README, task contract, architecture, threat model, test evidence and final audit. Treat all new architecture here as AI_PROPOSED_CONCEPT until explicit project authority promotes it. Never infer NEXY implementation from this lab's existence.