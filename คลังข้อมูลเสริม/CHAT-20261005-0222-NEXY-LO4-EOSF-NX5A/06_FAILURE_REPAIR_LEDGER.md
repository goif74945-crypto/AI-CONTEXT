# Failure -> Repair -> Re-test Ledger

| # | Detected failure/risk | Root cause | Smallest safe repair | Re-verification |
|---|---|---|---|---|
| 1 | TypeScript compile error in integration union | Code accessed `.record` on a branch that can be conflict-without-record | Explicitly narrow reconciliation result before selecting record | Full suite 32/32 PASS |
| 2 | Registry could not distinguish completed/in-flight/retryable duplicate | Seen mutation schema recorded identity but not execution state | Add `COMPLETED / IN_FLIGHT / FAILED_RETRYABLE`; suppress completed, freeze in-flight, route retryable through retry gate | Full suite 38/38 PASS |
| 3 | Cancellation only required compensation for SUCCEEDED effects | Job status was incorrectly used as proxy for whether an effect materialized | Define `hasExternalEffect` independently and require compensation for any materialized effect | Negative tests added; PASS |
| 4 | FNV-64 participated in critical equality | Compact fingerprint was convenient but collision-bearing | Critical identity changed to exact canonical structural seals; FNV retained telemetry-only | Full suite rerun; PASS after one test-contract update |
| 5 | Outbox replay did not distinguish PREPARED/COMMITTED/EMITTED/CANCELLED | Reconciliation returned generic replay | State-specific replay verdicts, cancelled reuse freeze, emitted suppression, committed resume | New integration/outbox tests PASS |
| 6 | Registry/outbox could disagree silently | Two stores were evaluated independently | Add explicit contradiction blocker `REGISTRY_OUTBOX_STATE_CONFLICT` | Negative integration test PASS |
| 7 | One test failed after API hardening | Expected exact object omitted new suppression evidence field | Update test expectation; implementation unchanged | 42/42 PASS |
| 8 | Packaging initially centralized code/tests | Did not satisfy per-concept co-location requirement strongly enough | Refactor each concept into its own `src/ + tests/ + DESIGN + EVIDENCE` folder | Layout regression 42/42 PASS |

No failure was hidden by weakening a safety rule.
