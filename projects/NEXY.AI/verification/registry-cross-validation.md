# Contract + FSM + Invariant Cross-Validation

## Result
**FAIL**

- contracts: **22**
- FSM/state models: **8**
- invariants: **40**
- cross-reference issues: **12**

Checks:
- Contract Registry entity references: PASS
- FSM source/state entity references: FAIL
- Invariant system references: PASS
- Requirement references across all three registries: PASS
- duplicate IDs inside each registry: PASS

## Review points intentionally preserved
- Contract schema differences are not auto-corrected.
- FSM namespace differences are not merged.
- Invariants remain NOT_EVALUATED until tests/evidence exist.
- Current implementation map is revision-bound to HEAD `9c9befd9fe255b0f9271e6e2b8c4bb2443a08089`.

## Next traceability stage
The next registry can now connect:

`REQUIREMENT → IMPLEMENTATION → TEST → EVIDENCE`

while using Contract/FSM/Invariant records as verification obligations.
