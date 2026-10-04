# 12 — Research Backlog

All items are proposals, not current NEXY requirements.

1. **Sequential evidence contracts** — add explicit group-sequential or always-valid inference so continuous monitoring does not silently invalidate alpha.
2. **Sample-ratio mismatch detector** — deterministic expected-vs-observed allocation checks with configurable exact/binomial thresholds.
3. **Novelty and interference controls** — represent carryover, network effects, marketplace interference, and treatment contamination.
4. **Segment invariants** — require predeclared protected/critical segments and freeze when aggregate success hides a severe segment regression.
5. **Metric provenance** — bind metric definitions to versioned event schemas and transformation code hashes.
6. **Causal assumptions record** — explicit DAG/assumption manifest for observational evidence where randomized assignment is impossible.
7. **Decision-cost model** — separate evidence state from reversible/irreversible product decision costs without making the final choice automatically.
8. **Experiment registry adapter** — append-only registry with contract hashes, evidence hashes, supersession links, and tombstones.
9. **Privacy budget integration** — model data minimization and privacy budgets as first-class experiment guardrails.
10. **Cross-experiment learning** — meta-analysis only when populations, contracts, metrics, and treatment semantics are proven compatible.
