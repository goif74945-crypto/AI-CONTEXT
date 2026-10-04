# Evidence — Metamorphic Contract Harness

- Evidence class: E1 static + E2 unit
- Final unit command: `python -m unittest -v test_src.py`
- Final result: PASS, 4 tests, 0 failures/errors.

## Red/green lineage
Initial RED occurred before implementation. Second RED exposed false PASS when zero checks executed. The harness now returns `NOT_VERIFIED` when `checks == 0`, followed by a clean regression run.

## Proven behaviors
- broken idempotency is detected;
- mapping-order invariance can be verified;
- mutation exceptions are evidence, not hidden skips;
- zero checks cannot become PASS.

## Limitation
Metamorphic relations must come from an authoritative contract. A bad relation can encode a bad expectation.
