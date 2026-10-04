# Known Limitations and Future Work

All items below remain PROPOSAL-level future work.

1. **No real NEXY integration**: adapters to NEXY contracts are not implemented because NEXY repositories are protected from mutation in this mission.
2. **MPWE complexity**: exact weighted set cover does not scale polynomially in the general case. A production design needs bounded solving and an explicit optimality flag.
3. **MVS relation provenance**: this prototype accepts explicit relations but does not implement an authority registry or provenance signature.
4. **CLL domain model**: only integer additive conservation is implemented. Non-additive conserved invariants require typed algebraic laws.
5. **BFK numeric canonicalization**: floats are intentionally rejected. A cross-language decimal/rational canonical standard would be required for broader use.
6. **SMS operator catalog**: only five constraint forms are implemented. Real policy mutation requires schema-aware operators and incident-derived mutations.
7. **No concurrency model**: prototypes are pure/synchronous; distributed race/interleaving behavior is outside scope and covered by other supplemental research.
8. **No E3+ evidence**: integration, E2E, runtime, deployment, and production behavior are NOT_VERIFIED because they were not authorized or executed.
9. **Collision screening is bounded**: folder enumeration and keyword search found no direct term collisions for the five selected themes, but semantic overlap under unrelated naming can still exist.
10. **Cryptographic authenticity is absent**: SHA-256 fingerprints are content identities, not signatures; authenticity requires a separate trust mechanism.
