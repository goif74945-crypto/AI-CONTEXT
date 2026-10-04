# Verification Plan

## Static checks

- Python bytecode compilation for every module and test file.
- Strict JSON parse for schema and example fixtures.

## Unit behavior

- canonical object-key order invariance;
- list-order sensitivity;
- float rejection;
- Unicode/whitespace normalization determinism;
- exact duplicate rejection;
- near-duplicate merge/reject path;
- missing evidence -> `NEEDS_EVIDENCE`;
- authority conflict -> `FREEZE_CONFLICT`;
- invalid approved-like status rejected at parse boundary;
- repeated evaluation serializes identically;
- duplicate catalog IDs rejected.

## CLI behavior

- `validate` returns PASS for a valid candidate;
- `evaluate` returns machine-readable advisory output;
- exit code is non-zero on malformed/invalid data.

## Regression gate

The full suite must pass after every repair. Verification evidence records the exact command and output.
