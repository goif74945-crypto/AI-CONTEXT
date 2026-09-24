# NEXY.AI Builder / Auditor Playbooks

## Build
- build-new-system.md
- modify-existing-system.md
- add-api-route.md
- add-state-transition.md
- add-storage-model.md
- add-queue-worker.md
- add-law.md
- add-ui-surface.md
- add-capability.md
- add-agent.md

## Audit
- audit-system.md
- audit-contract.md
- audit-authority.md
- audit-fsm.md
- audit-security.md
- audit-determinism.md
- audit-recovery.md
- audit-persistence.md
- audit-cross-system.md
- audit-release.md

## Global rule
Every playbook must resolve authority/scope, current HEAD, affected invariants, tests, evidence freshness and rollback before completion.

No playbook may convert:
- source prose into implementation PASS;
- file presence into runtime PASS;
- test-file presence into test PASS;
- stale evidence into current proof;
- UI visibility into authorization.
