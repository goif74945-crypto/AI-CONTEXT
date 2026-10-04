# Failure / Fix Record

F-001 decimal display truncation.

First full verification: TypeScript compilation PASS; 27/29 tests PASS, 2 FAIL. Constraint Slack displayed 0.199999 where six-decimal presentation should round to 0.2; Residual Work Mass displayed 0.099999 where it should round to 0.1.

Root cause: Q64.toDecimal(maxFractionDigits) truncated generated decimal digits instead of rounding the Q64.64 value at presentation precision.

Correction: replaced truncating rendering with deterministic half-even rounding and removed the remaining Number(...) conversion from padding logic.

Re-verification: clean dist, strict compile, numeric API scan, entire suite rerun. Final: 29/29 PASS; 0 fail; 0 skipped; 0 todo.
