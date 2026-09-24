# Failure record: coverage_check

Gate: `coverage_check`
Exit: `1`
Status: FREEZE / POLICY AUTHORITY UNRESOLVED

All preceding application/test gates passed, including full suite and coverage generation. The failure is emitted intentionally by `scripts/check-coverage.ts` because API coverage metrics fall on both sides of the 85% threshold and no authoritative metric is resolved.

This record must not be interpreted as a proven production-code defect.
