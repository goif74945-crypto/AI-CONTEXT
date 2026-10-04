# Future NEXY Integration Contract (proposal)

1. NEXY owns adapters and authority. Lab modules remain pure functions/classes.
2. Convert external values to Q64.64 at the boundary; never mix floating-point values into decision math.
3. Validate every normalized metric is in its documented range before calling a module.
4. Propagate explicit errors; do not silently saturate or substitute defaults.
5. Record raw Q64 values in decision evidence when replay determinism matters.
6. Do not treat `ELIGIBLE_FOR_FORMAL_PROMOTION_REVIEW` as promotion. Promotion remains an external Canon process.
7. Integration requires fresh E3/E4/E5 evidence in the exact NEXY revision; this lab's local tests are insufficient for that claim.
