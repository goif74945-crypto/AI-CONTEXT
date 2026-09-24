# NEXY Audit Playbook Contract

Audit rules:
- refresh exact repository/branch/HEAD before current-state claims;
- source existence ≠ implementation;
- implementation presence ≠ compliance;
- test file presence ≠ execution;
- test execution ≠ deployment proof;
- deployment proof is revision/environment/claim specific;
- future scope absence is not current DOC-C FAIL;
- CANDIDATE code mappings must be opened before use;
- unresolved authority/conflict may block verdict;
- allowed verdicts: PASS / FAIL / PARTIAL / BLOCKED / NOT_TESTED / NOT_VERIFIED / SCOPE / CONFLICT.

# Audit System

## INPUT
Target ontology entity/system ID.

## SEQUENCE
1. resolve authority/scope;
2. load requirements;
3. load implementation map and read mapped code;
4. load dependencies/dependents;
5. load contracts/FSM/invariants;
6. load test/evidence traceability;
7. load failure history;
8. compare expected vs observed behavior;
9. classify each requirement independently;
10. aggregate without hiding unknowns.

## ATTACKS
missing path, stub-only code, hidden fallback, stale evidence, forbidden dependency, unhandled failure, UI masking, out-of-scope promotion.

## OUTPUT
Requirement-level ledger + system verdict with explicit proof class and limitations.
