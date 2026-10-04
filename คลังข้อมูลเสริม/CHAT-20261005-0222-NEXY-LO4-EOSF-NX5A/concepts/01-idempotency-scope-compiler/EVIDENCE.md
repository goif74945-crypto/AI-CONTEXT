# ISC Evidence
- Source: `src/index.ts`.
- Focused tests: `tests/index.test.mjs` — 7 tests PASS in final 42-test suite.
- Positive: stable identity under payload key reordering; completed replay recognition.
- Negative: missing payload binding, missing mandatory scope, semantic alias, in-flight/retryable distinction, duplicate registry identity.
- Property evidence: integration property suite repeats canonical-order invariance across 100 cases.
- Truth boundary: standalone E1/E2 evidence only; NEXY persistence/provider semantics NOT_VERIFIED.
