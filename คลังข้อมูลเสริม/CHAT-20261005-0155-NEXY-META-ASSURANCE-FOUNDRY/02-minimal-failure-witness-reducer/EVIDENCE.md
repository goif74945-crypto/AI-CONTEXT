# Evidence — Minimal Failure Witness Reducer (MFWR)

Truth class: `REFERENCE_IMPLEMENTATION_EVIDENCE`, not NEXY production proof.

## Claims proved locally
- E1: `src/mfwr.py` compiles under Python 3.13.5.
- E2: 10 unit/negative tests pass.
- E2 differential: 98 required-subset failure cases were checked by `deep_validation.py`; every returned witness reproduced failure and was 1-minimal.
- E3-local: root integration smoke imports MFWR and reduces a representative reproducible failure.

## Negative paths covered
- initial case does not fail;
- unstable/nondeterministic oracle;
- evaluation budget exhaustion;
- invalid oracle return type / invalid budget;
- JSON-incompatible witness items;
- no single-element removable survivor in successful result.

## Exact local commands
```text
python3 -m compileall -q .
python3 -m unittest discover -s 02-minimal-failure-witness-reducer/tests -p 'test_*.py'
python3 integration_smoke.py
python3 deep_validation.py
```

## Limitations
- 1-minimal does not mean globally minimum-cardinality witness.
- The integrating harness remains responsible for supplying a meaningful failure oracle.
- Oracle stability is checked by duplicate evaluation per uncached candidate; this detects observed disagreement, not philosophical proof of determinism.
- No live NEXY integration is claimed.
