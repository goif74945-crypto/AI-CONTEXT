# PLAYBOOK — Add or Modify LAW

## PRECONDITIONS
- Proposed law is authorized by the correct authority.
- Scope is explicit: USER LAW, system law, policy, resource law, temporal law, etc.
- No older/historical law is being revived through alias confusion.
- Supersession/conflict graph reviewed.

## REQUIRED CONTEXT
- governance authority/scope/supersession/conflicts;
- LAW ontology entity;
- affected requirements;
- invariants;
- release/FSM/security behavior;
- implementation law engine;
- tests/evidence obligations.

## IMPLEMENTATION SEQUENCE
1. State the law as a deterministic predicate/rule.
2. Define authority and precedence.
3. Define applicability scope.
4. Define inputs/state it may inspect.
5. Define exact block/freeze/error result on violation.
6. Define whether evaluation occurs precheck, prerelease, runtime, build-time, or multiple.
7. Define audit/provenance.
8. Define version/supersession semantics.
9. Implement without hidden heuristic bypass.
10. Add allow/block boundary tests.
11. Add conflict tests with adjacent laws.
12. Run release/FSM/security regression.

## FORBIDDEN
- free-text law with no executable interpretation when enforcement is required;
- ad-hoc owner force bypass not authorized by Canon;
- silent precedence changes;
- unversioned replacement of old law;
- presentation/UI override of LAW.

## DONE
The law's authority, precedence, enforcement points, failure semantics and required negative tests are proven.
