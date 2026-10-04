# Verification and Evaluation Matrix

Verification layers: static validity; unit behavior; integration boundaries; end-to-end objectives; adversarial cases; regression; operational recovery.

Every acceptance criterion maps to criterion_id, test_id, environment, preconditions, action, expected result, observed result, evidence locator, and status.

Allowed status: PASS | FAIL | BLOCKED | NOT_RUN | NOT_VERIFIED.

AI eval dimensions include factual grounding, instruction hierarchy compliance, tool selection correctness, scope adherence, refusal correctness, recovery from tool failure, provenance preservation, structured-output correctness, and explicit latency/cost budgets where required.

A test is invalid if it checks only text existence when behavior is required, mocks the exact boundary claimed as real, ignores negative paths, or treats model self-report as evidence.
