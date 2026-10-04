# Evidence — MCFG

- TDD RED: original interface stub raised `NotImplementedError` under the pre-written tests.
- Focused tests verify exact expected cut sets, invalid/oversized inputs and input-order determinism.
- Property test `test_random_small_instances_match_bruteforce` checks 80 deterministic random small instances against an independent exhaustive powerset/combinations implementation.
- Property tests verify hitting and inclusion-minimality invariants directly.

Claim supported: the local Python reference matches the independent brute-force oracle over the executed bounded corpus. This does not prove performance or correctness for unbounded inputs.
