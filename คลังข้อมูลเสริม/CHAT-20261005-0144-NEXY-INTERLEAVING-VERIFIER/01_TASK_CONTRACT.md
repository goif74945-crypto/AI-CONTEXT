# Task Contract — Deterministic Interleaving Verifier Lab

Status: LOCKED FOR THIS EXECUTION
Authority: explicit user request + AI-CONTEXT execution rules
Classification: AI-PROPOSED auxiliary engineering artifact

## OBJECTIVE
Create a new, non-duplicative, executable auxiliary system in AI-CONTEXT that can help future NEXY.AI work by exhaustively exploring a bounded deterministic action state space and proving whether all legal interleavings preserve invariants and converge to one canonical final state.

## REQUIRED OUTPUT
1. Architecture/design contract.
2. Safe declarative action model; no eval/exec/user code execution.
3. Exact bounded state-space explorer with state merging.
4. Deterministic PASS/FAIL/FREEZE semantics.
5. Divergence and violation witnesses.
6. Static conflict/access analysis.
7. Machine-readable CLI report.
8. Unit/regression/negative tests.
9. Fixtures/examples.
10. Verification evidence and final audit.
11. Durable temporary/resumption memory.

## IN SCOPE
Only files under:
`คลังข้อมูลเสริม/CHAT-20261005-0144-NEXY-INTERLEAVING-VERIFIER/`

## OUT OF SCOPE / IMMUTABLE PROHIBITIONS
- No write to any repository whose name contains `NEXY.AI`.
- No modification of existing sibling labs.
- No claim that this proposal is current NEXY architecture or implementation.
- No deployment or production integration.
- No arbitrary code execution from model inputs.
- No probabilistic/random exploration used to justify PASS.
- No silent truncation of the state space.
- No approximation presented as proof.

## SUCCESS INVARIANTS
- Same canonical input semantics -> same machine report/fingerprint.
- PASS only when the complete bounded reachable state space is explored within declared limits and all terminal states agree while all invariants/preconditions remain legal.
- Limit exhaustion -> FREEZE / NOT_VERIFIED, never PASS.
- Invalid graph/schema/operation -> FREEZE with deterministic diagnostics.
- Unordered conflicting actions are surfaced.
- Divergence contains at least two reproducible schedule witnesses.
- Intermediate invariant violations fail even if terminal state later reconverges.
- Core has no network, clock, randomness, filesystem mutation, subprocess, environment, eval, or hidden I/O.

## REQUIRED EVIDENCE
- E1: Python compile/static importability.
- E2: executed unit/regression/negative tests.
- E0/read-back: GitHub paths exist and critical source blobs match the tested local artifacts.
- E3+ NEXY integration: explicitly NOT_VERIFIED.

## STOP CONDITIONS
FREEZE the affected claim if:
- input semantics are invalid;
- dependencies are cyclic/missing;
- the exploration cap is exceeded;
- operation semantics cannot be evaluated deterministically;
- exact tested-source identity cannot be established for an E2 claim.

## ACCEPTANCE
All in-scope tests pass, negative paths behave fail-closed, GitHub read-back matches tested source for critical executable artifacts, and no protected repo was modified.
