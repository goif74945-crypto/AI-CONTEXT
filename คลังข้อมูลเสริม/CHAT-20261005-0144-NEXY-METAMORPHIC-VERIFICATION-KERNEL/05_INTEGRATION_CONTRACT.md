# Future NEXY Integration Contract

**Status: DESIGN ONLY / NEXY INTEGRATION NOT VERIFIED**

## Adapter interface
An integrator implements a callable:

```python
(case: Case) -> Observation
```

The adapter is responsible for translating normalized MVK input into an authorized NEXY test path and translating externally observable NEXY behavior into `Observation`.

## Required adapter rules
- Never embed credentials in Case/Observation.
- Preserve exact target revision/environment in observation metadata outside secret fields.
- Normalize release/freeze state explicitly.
- Normalize externally visible side effects into stable identifiers.
- Do not infer evidence that NEXY did not emit.
- Fail rather than fabricate missing fields required by the chosen relation.

## Suggested CI placement
1. Unit tests.
2. Existing integration tests.
3. MVK relation suite against a deterministic test adapter/environment.
4. E2E/runtime evidence where required.
5. Release gate consumes MVK results as evidence, not as sole authority.

## Non-goal
MVK must not bypass `NEXY::JUDGE`, USER LAW, or existing release/freeze boundaries. It tests behavior; it does not become a higher authority.
