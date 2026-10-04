# NEXY EPC Proof Resilience Fracture Fabric 20 (PRFF20)

Status: **Lo4 AI proposal / standalone / non-canonical / not integrated into NEXY.AI**

PRFF20 answers a question not covered by simple evidence counts: **if evidence/root/support components disappear or fail, how many failures are required to fracture the proof, and what exact cutsets cause the fracture?**

It contains exactly twenty executable mechanisms covering strict DAG validation, root and support-channel diversity, evidence vertex/edge connectivity, minimum cut certificates, dominators, bridges, exact bounded ablation, minimum-cut families, cross-claim bottlenecks and a non-authoritative review-readiness certificate.

The package intentionally does not decide EPC KEEP/CUT and does not mutate NEXY state. Its strongest output is `READY_FOR_JUDGE_LAW_REVIEW_ONLY`.

## Build
```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j2
ctest --test-dir build --output-on-failure
./build/prff_example
```

## Source layout
- `include/nexy_prff/q64.hpp` — checked Q64.64 substrate.
- `include/nexy_prff/prff.hpp` — strict public data model.
- `src/prff.cpp` — 20 mechanisms and deterministic algorithms.
- `tests/test_main.cpp` — adversarial/unit cases.
- `tests/property_main.cpp` — Q64, permutation, mutation and brute-force min-cut oracles.
- `tests/sanitizer_stress.cpp` — bounded ASan-friendly stress surface.
- `examples/integration_example.cpp` — non-authoritative integration example.
- `evidence/` — compiler, sanitizer, replay and hash evidence.

## Critical authority sentence
**PRFF evaluates proof topology. JUDGE/LAW retain decision authority. PRFF never promotes itself or a candidate.**
