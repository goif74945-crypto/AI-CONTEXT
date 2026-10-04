# Threat / Failure Model

> Scope: the five auxiliary prototypes only. This is not a security certification for NEXY.AI.

| Threat / failure | Mechanism | Current mitigation | Residual limitation |
|---|---|---|---|
| Contradictory component guarantees | C1 | freeze on opposite literal | no richer theorem proving / implication logic |
| Hidden assumption unsatisfied | C1 | unresolved assumptions returned explicitly | contract completeness depends on caller |
| Secret/private data reaches external/public sink through multiple tools | C2 | taint propagation + sink findings | capability/taint labels must be trustworthy upstream |
| Untrusted input reaches execution/protected mutation | C2 | UNTRUSTED propagation + validator boundary | validator implementation is not proven here |
| Low-trust authority drives privileged mutation | C2 | confused-deputy finding | identity/authn itself is outside prototype |
| Reusing evidence after code/runtime/provider drift | C3 | policy per context dimension; MUST_EQUAL / REVERIFY / CAN_DIFFER | policy author remains authority for dimension semantics |
| Caller omits changed context dimension to force PORTABLE | C3 | all observed context dimensions must be governed or FREEZE | cannot detect a dimension never supplied by either side |
| Stale/future-dated proof | C3 | expiry boundary + collection/evaluation consistency | trusted clock/source timestamp is external |
| User correction overgeneralized into global behavior | C4 | bounded selector ≥2 dimensions; global requires USER_LAW | semantic quality of structured correction is external |
| Contradictory corrections | C4 | deterministic conflict checks | not a full SMT solver; complex semantic contradictions may escape |
| Flaky failure oracle yields bogus minimal repro | C5 | evaluate each candidate twice; FREEZE on mismatch | two confirmations cannot prove permanent determinism |
| Minimizer claims global minimum incorrectly | C5 | output says 1-minimal, not globally minimum | ddmin may return a larger-than-global minimum |
| Non-portable JSON identity | shared | reject NaN/Infinity; detect key collisions; canonical serialization | Unicode semantic normalization intentionally not performed |
| Output tampering | shared | content fingerprint | no signing/key infrastructure in this prototype |
