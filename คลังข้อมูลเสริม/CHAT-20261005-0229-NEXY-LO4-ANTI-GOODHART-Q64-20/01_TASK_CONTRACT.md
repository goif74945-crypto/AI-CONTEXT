# Task Contract — Lo4 Anti-Goodhart Q64 Foundry 20

## objective
Produce a reusable, deterministic, dependency-minimal reference package implementing exactly 20 Anti-Goodhart / Goal-Integrity engines for potential future NEXY integration.

## target
`คลังข้อมูลเสริม/CHAT-20261005-0229-NEXY-LO4-ANTI-GOODHART-Q64-20` in `goif74945-crypto/AI-CONTEXT`.

## authorized_scope
Create new files under the target namespace; execute local tests against exact candidate bytes; publish verified bytes; re-fetch published artifacts.

## protected_scope
All pre-existing paths outside the namespace and every repository whose name contains `NEXY.AI`.

## success_invariants
1. Exactly 20 named Lo4 concepts are documented and implemented.
2. Every decision-relevant real-valued computation uses checked signed Q64.64.
3. No Python binary float is accepted by authoritative APIs.
4. Overflow never wraps or saturates.
5. Deterministic canonical inputs yield deterministic outputs.
6. Every engine has at least one positive and one negative/adversarial test.
7. Cross-engine integration test exists.
8. Failure/freeze semantics are explicit.
9. No network/provider/secret dependency.
10. Persisted code is bound to test evidence by file hashes.
11. GitHub read-back confirms required artifacts exist after publication.
12. Every artifact remains explicitly Lo4 proposal-only.

## required_evidence
- E1: `python -m compileall`
- E2: unit + boundary + adversarial tests
- E3: cross-engine integration pipeline
- deterministic repeated-run digest
- SHA-256 manifest for tested files
- repository read-back

## stop_conditions
Freeze rather than claim completion if:
- protected scope would be mutated;
- Q64.64 overflow/rounding contract is violated;
- required tests fail;
- persisted bytes cannot be matched to tested bytes;
- integration/deployment is being inferred without evidence.
