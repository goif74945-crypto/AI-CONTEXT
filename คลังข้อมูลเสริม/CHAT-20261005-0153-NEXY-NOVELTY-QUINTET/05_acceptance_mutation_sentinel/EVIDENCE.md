# Evidence — Acceptance Mutation Sentinel

- Evidence class: E1 static + E2 unit
- Final unit command: `python -m unittest -v test_src.py`
- Final result: PASS, 5 tests, 0 failures/errors.

## Red/green lineage
Initial RED occurred before implementation. Second RED exposed false PASS with zero mutators. The engine now reports `NOT_VERIFIED` when no mutations challenge the gate; regression passed afterward.

## Proven behaviors
- strong gates kill critical mutations;
- weak gates expose surviving corruptions;
- invalid baselines are rejected as configuration errors;
- mutators cannot alter caller baseline in place;
- zero mutations cannot earn PASS.

## Limitation
A 100% kill rate is scoped to the supplied mutation operators. It is not proof against unmodeled corruption classes.
