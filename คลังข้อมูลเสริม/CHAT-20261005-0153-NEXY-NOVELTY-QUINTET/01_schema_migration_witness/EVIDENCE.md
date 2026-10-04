# Evidence — Schema Migration Witness

- Evidence class: E1 static + E2 unit
- Final unit command: `python -m unittest -v test_src.py`
- Final result: PASS, 5 tests, 0 failures/errors.
- Static command: aggregate `python -m compileall -q <pack-root>`
- Static result: PASS.

## Red/green lineage
Initial RED: import failed before implementation existed. Second RED intentionally exposed an unsafe false-PASS: empty witness corpus returned PASS. The implementation was changed so zero witnesses yield `NOT_VERIFIED`; full regression then passed.

## Proven behaviors
- reversible rename round trip can PASS on explicit witnesses;
- irreversible field loss is detected;
- defaults do not overwrite existing values;
- unsupported operations fail closed;
- empty witness corpora cannot claim PASS.

## Limitation
This proves only the explicit witness corpus and supported operation semantics. It is not a universal schema theorem prover.
