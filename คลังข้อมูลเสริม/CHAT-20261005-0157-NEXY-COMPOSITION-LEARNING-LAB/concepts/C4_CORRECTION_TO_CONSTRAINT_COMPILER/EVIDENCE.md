# C4 Evidence

Standalone evidence achieved: **E1 + E2**.

Executed cases include:
- deterministic compilation independent of mapping order;
- bounded selector does not leak into neighboring context;
- compliant output PASS;
- regression FAIL with exact violation record;
- overbroad bounded scope rejected;
- global scope rejected without USER_LAW;
- duplicate/conflicting correction behavior;
- conflicting equalities;
- exists/not-exists conflict;
- malformed `supersedes` rejection.

The prototype does not verify whether a correction itself is true or authoritative. That promotion decision belongs upstream to NEXY authority/evidence logic.
