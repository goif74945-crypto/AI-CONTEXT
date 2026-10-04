# Evidence — Determinism Divergence Bisector

- Evidence class: E1 static + E2 unit
- Final unit command: `python -m unittest -v test_src.py`
- Final result: PASS, 4 tests, 0 failures/errors.

## Red/green lineage
Initial RED occurred because the implementation API did not exist. GREEN then passed all defined behaviors.

## Proven behaviors
- configured volatile metadata does not create false divergence;
- first semantic divergence is localized;
- dependency frontier is surfaced;
- identical traces report `EQUIVALENT`;
- unequal trace length is distinguished from content divergence.

## Limitation
Equivalence is relative to the canonicalization policy. Incorrectly classifying an authority-bearing field as volatile can hide a real difference.
