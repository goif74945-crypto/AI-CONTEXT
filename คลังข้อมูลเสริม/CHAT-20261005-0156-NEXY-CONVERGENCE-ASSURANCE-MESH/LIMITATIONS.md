# Known Limitations

1. **CNS is finite-test noninterference, not a universal formal proof.** Its PASS is bounded to supplied mutations and decision function behavior.
2. **ICG assumes the caller provides the admissible interpretation set.** It does not infer natural-language meanings or decide which interpretations are legally admissible.
3. **EAP optimizes a deterministic set-cover model.** It does not estimate probabilistic test flakiness, wall-clock parallelism, or monetary provider pricing unless encoded as deterministic cost.
4. **REC proves equality of declared resume-critical state and reconstructed next-action behavior.** Choosing the correct critical/ephemeral partition remains an integration responsibility.
5. **IEQE models independence through explicit producer/failure-domain/derivation metadata.** Missing or falsely declared provenance can invalidate the independence conclusion.
6. No live NEXY implementation repository was mutated or instrumented, so actual integration compatibility is design-level + standalone contract evidence only.
7. No E4/E5/E6 evidence exists. There is no browser E2E, target-runtime operational, or deployment claim.
