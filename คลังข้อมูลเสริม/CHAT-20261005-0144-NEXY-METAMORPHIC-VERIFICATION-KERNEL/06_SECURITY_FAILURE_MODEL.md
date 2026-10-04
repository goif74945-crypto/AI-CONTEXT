# Security and Failure Model

## Threats
- Untrusted payload objects with nondeterministic or executable repr behavior.
- Malicious adapter returning wrong types.
- Relation definitions whose mutators silently broaden authority.
- Semantic-equivalence claims that are not actually equivalent.
- Secret leakage in case metadata or evidence logs.
- Stateful adapters causing replay drift.

## Controls implemented
- Canonicalizer supports a strict allowlist of structural types and rejects arbitrary objects.
- Non-finite floats are rejected.
- Immutable public Case/Observation mapping surfaces use defensive copies + mapping proxies.
- Mutator/adapter/oracle exceptions are captured as `ERROR`, never PASS.
- Critical monotonicity relations test for newly gained side effects.
- Duplicate relation IDs are rejected within a report.

## Residual risks
- A dishonest adapter can lie about target behavior.
- A poorly selected projection can hide meaningful semantic drift.
- A test author can falsely label context as irrelevant or prompts as semantically equivalent.
- Side-effect strings are normalized claims, not cryptographic receipts.

## Required future hardening for production-grade integration
- Signed/traceable effect receipts.
- Exact revision/environment binding.
- Adapter conformance suite.
- Schema version in canonical hash domain.
- Resource/time bounds.
- Controlled sandbox for target execution.
