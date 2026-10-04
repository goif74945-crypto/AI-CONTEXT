# MMCRC20 Test Evidence

This evidence proves only the standalone MMCRC20 bytes identified by `SHA256SUMS`. It does not prove live provider behavior, NEXY runtime integration, deployment, or provider availability.

Executed evidence:
- GCC C++20 with `-Wall -Wextra -Wpedantic -Werror`: 2,646 checks PASS.
- Clang C++20 with same warning policy: 2,646 checks PASS.
- GCC integration: PASS, all 20 mechanisms invoked.
- Clang integration: PASS, byte-identical output to GCC.
- ASan + UBSan unit: PASS, stderr 0 bytes.
- ASan + UBSan integration: PASS, stderr 0 bytes.
- CMake/CTest: 2/2 PASS.
- static policy scan: no authoritative float/double, RNG, wall-clock, network socket/process execution, or repo/Core mutation surface in include/src/examples.
- deterministic integration replay: 100/100 identical stdout SHA-256.

Integrated 20-mechanism capsule:
`REPLAY_SHA256=8dd313a54504701c624fd6da4b2b96b6cd66a24333fef1576f1ace0651cd849e`
`AUTHORITY_MUTATION_ALLOWED=false`
`PROMOTION_ALLOWED=false`

Negative paths include missing adapter fields, unsupported modes, invalid timeout/context, provider mismatch, health divergence, cancel failure/post-cancel effects, malformed/missing confidence, malformed evidence, semantic response divergence, incomplete truncation boundary fixtures, unsafe retry, failover insufficiency, unapproved model drift, invalid Q64 scores/weights, malformed capsule identity and non-compensatory hard-gate failure.
