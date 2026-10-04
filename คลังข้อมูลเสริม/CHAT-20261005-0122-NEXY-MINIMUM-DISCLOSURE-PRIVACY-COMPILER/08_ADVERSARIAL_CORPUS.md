# Adversarial Corpus Guide

Machine-readable scenarios live in `fixtures/adversarial_cases.json`.

The corpus is intentionally policy-centric rather than prompt-refusal-centric. The expected control is enforced by deterministic code, not by hoping a model declines a bad instruction.

Coverage axes:
- credential prompt injection;
- unknown recipient;
- unnecessary private field;
- purpose drift;
- missing private consent;
- secret-to-external attempt;
- retention inflation;
- rule-order nondeterminism.

Future corpus should add:
- cross-tenant field confusion;
- recipient registry stale/revoked state;
- transform downgrade attempts;
- malicious field-name collisions;
- batch tasks with mixed purposes;
- multi-recipient fan-out;
- derived/inferred sensitive data;
- regional policy conflict;
- deletion-proof failure;
- provider setting drift after plan compilation.
