# Concept 4 — Benefit Regression Judge
AI-PROPOSED / NON-GOVERNING

**Problem:** technically correct changes can make the system worse for users.

**Contract:** declare axes, direction, criticality, minimum meaningful improvement, and tolerated regression before comparison.

**Core invariant:** missing observations are inconclusive, unchanged work is not automatically beneficial, and critical regression cannot be averaged away by improvement elsewhere.

**Why it can help NEXY:** it adds an explicit user-value regression gate between verified engineering output and adoption discussion, without pretending exact observed deltas are statistical causal evidence.

**Implementation:** `src/benefit_regression.ts`.
**Tests:** `tests/benefit_regression.test.mjs`, malformed/tradeoff adversarial tests, integration test.
**Evidence:** final direct test record and demo.
