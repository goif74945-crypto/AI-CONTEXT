# NEXY.AI Audit Playbooks

## Purpose
Adversarial audit procedures that test whether NEXY architecture, implementation and evidence agree.

Audit playbooks never infer PASS from file/symbol presence.

## Mandatory audit preflight
1. Pin repo/branch/HEAD when implementation is involved.
2. Resolve authority/scope/supersession/conflicts.
3. Resolve requirement IDs.
4. Resolve ontology entities and dependency neighborhood.
5. Resolve contracts/invariants/FSM/security/state/event/config records.
6. Resolve implementation mappings at the exact observed HEAD.
7. Resolve required evidence class.
8. Search for bypass/contradiction/negative paths.
9. Produce evidence-backed findings and exact unknowns.

## Canonical audits
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

## Finding statuses
PASS / FAIL / PARTIAL / BLOCKED / NOT_VERIFIED / UNKNOWN / CONFLICT / MISSING / SCOPE

## Audit law
Absence from a single search is not MISSING.
Presence is not IMPLEMENTED.
Implementation is not VERIFIED.
Verification is not DEPLOYMENT.
