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

# Audit Authority

## SEQUENCE
1. identify claim/question type: normative build / implementation / runtime / deploy / physical;
2. determine scope;
3. load authority graph;
4. inspect claim-level supersession;
5. inspect conflict registry;
6. reject authority inversion.

Critical checks:
- DOC-D does not add obligations excluded by DOC-C;
- implementation does not redefine spec;
- older claim does not overwrite newer claim;
- UI/SWARM/Lo2 does not become final truth authority;
- OWNER actions stay within legal procedures.

Output unresolved authority as CONFLICT/BLOCKED, not guessed precedence.
