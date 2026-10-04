# CCC Evidence
- Source: `src/index.ts`.
- Focused tests: 6 PASS.
- Positive: subtree cancellation + compensation collection.
- Negative: untracked effect, unknown parent, FAILED effect without compensation.
- Running job with a materialized effect still requires compensation.
- Property: result invariant to input ordering.
- Stress: 5,000 order-invariance cancellation checks PASS.
