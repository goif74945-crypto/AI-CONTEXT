# Risk Register

| Risk | Impact | Control | Residual status |
|---|---|---|---|
| Behavioral fingerprint misses semantic duplicate | Medium | Treat result as advisory; threshold conservative; no auto-delete/merge | OPEN |
| Mined invariant is spurious | High | EXPERIMENTAL quarantine + counterexample challenge + human review only | CONTROLLED |
| Least capability closure is not least privilege in a real runtime | High | Model only declared dependencies; production adapter audit required | NOT_VERIFIED |
| Distilled guard overfits labeled examples | High | Guard remains EXPERIMENTAL; require independent regression/adversarial corpus | CONTROLLED |
| Tournament metrics encode bad incentives | High | Hard constraints dominate; evidence required; tie freezes; weights remain explicit | CONTROLLED |
| Prototype scale insufficient | Medium | No production SLA claim | OPEN |
| NEXY integration drifts from future implementation | High | Adapter-only integration proposal; revalidate against exact future head | OPEN |
