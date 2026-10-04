# Failure → Fix → Re-test Log

## Failure observed
First full unit run failed exactly one test:
`test_q64.Q64Tests.test_mul_div`

Observed raw values:
- actual: `9223372036854775807`
- expected by the original test: `9223372036854775808`

## Root cause
The implementation explicitly uses fixed-point truncation toward zero. `Q64.from_ratio(2,3)` cannot represent exact 2/3, so multiplying its truncated representation by 3/4 is one raw Q64 ULP below exact 1/2. The arithmetic implementation matched the declared semantics; the test incorrectly required real-number equality after quantization.

## Correction
- Kept truncation semantics unchanged.
- Replaced the invalid equality assertion with a one-raw-ULP error-bound assertion for the non-dyadic composition.
- Added an exact dyadic product assertion (`1/2 × 1/2 = 1/4`).
- Added tests proving float constructor inputs are rejected.
- Added an AST static policy scan rejecting runtime float literals and network imports.

## Re-test
Full verification rerun passed:
- compileall: PASS;
- 20 unit/integration tests: PASS;
- adversarial boundary samples: PASS;
- static policy scan: PASS;
- byte replay determinism: PASS.
