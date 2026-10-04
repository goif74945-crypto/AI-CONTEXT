# NEXY Information Acquisition Foundry — NIAF-20

**Status:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`  
**Work code:** `CHAT-20261005-0309-NEXY-LO4-NIAF-Q64-20`  
**Platform-native chat ID:** `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`

NIAF-20 is a standalone deterministic reference package for choosing **what clarification or evidence is worth acquiring next** when a NEXY-compatible pipeline has unresolved information. It does not decide truth, mutate CORE state, bypass verification, release FINAL output, or promote itself into Canon.

The observed NEXY CIRL surface already knows how to return `WAIT_FOR_DATA_CLARITY`. NIAF-20 explores the next missing step: rank acquisition actions by expected information gain versus user burden, privacy, latency, irreversibility and staleness, then either propose a bounded acquisition action or package a freeze recommendation.

## What is implemented

Twenty C++20 subsystems, all using checked signed Q64.64 arithmetic:

1. Epistemic Entropy Ledger
2. Marginal Information Gain
3. Value-of-Information Scorer
4. User Burden Budget
5. Privacy Cost Meter
6. Latency Budget Meter
7. Irreversibility Risk Guard
8. Ambiguity Partition Resolver
9. Question Novelty Filter
10. Answer Sensitivity Ranker
11. Missing Variable Impact Ranker
12. Evidence Conflict Probe Ranker
13. Exact Probe Portfolio Optimizer
14. Stop-or-Ask Frontier
15. Explicit-Tick Staleness Decay
16. Evidence Saturation Detector
17. Calibration Loss Tracker
18. Batch Query Composer
19. Fallback Freeze Evidence Packager
20. Acquisition Envelope Compiler

## Hard authority boundary

Every produced envelope is labeled:

- `authority=Lo4_AI_PROPOSAL_ONLY/NON_GOVERNING`
- `canon_effect=NONE`
- `can_mutate_core_state=false`

The canonical envelope compiler rejects attempted authority-label escalation, Canon-effect escalation, or a true CORE-mutation flag.

## Build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j2
ctest --test-dir build --output-on-failure
./build/niaf_example
python3 scripts/static_audit.py
```

The sealed verification evidence records GCC 14.2, Clang 17 ASan/UBSan, 29 behavioral groups, 20,001 Q64 identity iterations, 2,000 portfolio property iterations, 50 replay runs with one unique SHA-256, static forbidden-construct scanning, and byte-identical GCC/Clang example output.

## Integration status

`NEXY.AI` integration is **NOT VERIFIED and NOT PERFORMED**. The package is intentionally isolated in AI-CONTEXT supplemental storage. A future adoption must be an explicit promotion/integration process against a named NEXY revision and must preserve CORE/JUDGE/LAW authority.
