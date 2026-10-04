# Counterfactual Verification Engine
A happy-path PASS is insufficient. For each requirement test: valid case, near-miss invalid case, boundary, stale state, concurrency, permission denied, dependency unavailable, and contradictory context.

Metamorphic invariants:
- duplicate evidence never increases authority;
- lowering permission never increases capability;
- stale evidence never outranks fresh equivalent evidence;
- removing optional context never removes mandatory constraints;
- idempotent retries never duplicate side effects;
- ordering independent inputs never changes semantic result.

Evidence binds input, observed output, environment/state identifier, time, and expected invariant. If a forbidden counterfactual succeeds, freeze promotion even when happy paths pass.
