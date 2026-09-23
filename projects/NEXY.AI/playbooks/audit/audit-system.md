# PLAYBOOK — Audit System

## PURPOSE
Determine whether one NEXY system/subsystem satisfies its current governing requirements without hiding missing proof.

## INPUT
- target ontology ID;
- repo/branch/HEAD when implementation is in scope;
- authority/scope context.

## PROCEDURE
1. Resolve canonical entity/aliases/parent/dependents.
2. Resolve current vs future/historical scope.
3. Collect governing requirements.
4. Collect dependency edges.
5. Collect contracts/invariants/FSM/security/state/events/config.
6. Refresh code mapping if implementation snapshot is stale.
7. Trace entry points and mutation owners.
8. Compare expected behavior vs implementation semantics.
9. Inspect failure/recovery paths.
10. Inspect tests and evidence by required class.
11. Search for bypass routes and duplicated alternative implementations.
12. Produce requirement-level verdicts.
13. Collapse shared defects into root causes.

## ADVERSARIAL QUESTIONS
- Can another module bypass this system?
- Can stale/invalid state cross its boundary?
- Can failure be masked as success?
- Can an unauthorized actor mutate its state?
- Are async/retry/idempotency semantics explicit?
- Does evidence prove the claim at the current HEAD?

## OUTPUT
- system verdict;
- finding IDs;
- requirement ledger deltas;
- proof gaps;
- change-impact neighborhood;
- exact evidence limits.
