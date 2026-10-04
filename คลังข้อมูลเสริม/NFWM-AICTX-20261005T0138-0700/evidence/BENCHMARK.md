# NFWM Synthetic Benchmark Evidence

## Claim boundary

This is a one-run local synthetic observation, not a portable performance SLA and not NEXY.AI runtime evidence.

## Scenario

- 10,000 ordered events.
- 9,998 irrelevant `NOISE` events.
- one `RUNNING → FREEZE` event at sequence `4321` with incident linkage.
- one `RELEASE` event at sequence `8765` in the same trace/run scope.

## Observed result

```text
analysis_seconds=0.002580
minimize_seconds=0.045468
source_events=10000
witness_events=2
witness_seqs=[4321, 8765]
one_minimal=True
witness_hash=5093f835ac47bbf09aaea4f793b860bfcdd91c4790904423a1e0dfc8b832df43
```

## Interpretation

The result demonstrates that the current implementation can reduce a sparse two-event invariant failure embedded in 10,000 events to a two-event witness in this sandbox. It does not establish worst-case complexity, production throughput, or distributed-trace performance.
