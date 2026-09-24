# NEXY.AI Builder / Auditor Playbooks

## Build
- add-agent.md
- add-api-route.md
- add-capability.md
- add-event-contract.md
- add-law.md
- add-queue-worker.md
- add-state-transition.md
- add-storage-model.md
- add-ui-surface.md
- build-new-system.md
- change-config.md
- modify-existing-system.md

## Audit
- audit-authority.md
- audit-contract.md
- audit-cross-system.md
- audit-determinism.md
- audit-fsm.md
- audit-persistence.md
- audit-recovery.md
- audit-release.md
- audit-security.md
- audit-system.md

## Registry contract
- `registry.json` is the machine-readable discovery registry.
- `registry.schema.json` is the schema for the registry.
- Registry paths MUST match the real filesystem; unregistered or dangling playbook paths are invalid.

## Selection rule
Choose the narrowest playbook matching the task. Compose playbooks only when the task crosses explicit boundaries. Selection is by registered `task_type` + `role`, not filename similarity.

## Global rule
Every playbook must resolve authority/scope, current HEAD, affected invariants, tests, evidence freshness and rollback before completion.

No playbook may convert:
- source prose into implementation PASS;
- file presence into runtime PASS;
- test-file presence into test PASS;
- stale evidence into current proof;
- UI visibility into authorization.
