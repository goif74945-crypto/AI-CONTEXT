# NEXY.AI Build Playbooks

## Purpose
Reusable, project-specific build procedures for AI agents modifying or extending NEXY.

These playbooks are **not authority sources**. They orchestrate the authority/requirement/graph/contract/invariant/evidence registries.

## Mandatory preflight for every playbook
1. Resolve current user task and authorized scope.
2. Read `projects/NEXY.AI/governance/` for authority/scope/supersession/conflicts relevant to the target.
3. Resolve requirement IDs in `requirements/requirements.jsonl`.
4. Resolve entities/dependencies in `ontology/` + `graphs/dependency-graph.json`.
5. Check `implementation/INDEX.md` pinned repo/branch/HEAD.
6. If actual target HEAD differs from the implementation map snapshot, refresh implementation/code mappings before relying on them.
7. Resolve contracts, invariants, FSMs, security/state/event/config records affected by the change.
8. Build a change-impact set before mutation.
9. Execute only authorized mutations.
10. Prove with the evidence class required by the affected requirements.

## Build status
A playbook run may end only as:
PASS / FAIL / PARTIAL / BLOCKED / NOT_VERIFIED / CONFLICT.

## Canonical playbooks
- `build-new-system.md`
- `modify-existing-system.md`
- `add-api-route.md`
- `add-state-transition.md`
- `add-storage-model.md`
- `add-queue-worker.md`
- `add-law.md`
- `add-ui-surface.md`
- `add-capability.md`
- `add-agent.md`
- `add-event-contract.md`
- `change-config.md`

## Core law
No playbook can turn design presence or code presence into a PASS.
Verification/evidence remains authoritative for completion claims.
