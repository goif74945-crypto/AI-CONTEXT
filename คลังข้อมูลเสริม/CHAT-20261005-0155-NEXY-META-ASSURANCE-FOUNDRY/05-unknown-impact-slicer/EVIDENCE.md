# Evidence — Unknown Impact Slicer (UIS)

Truth class: `REFERENCE_IMPLEMENTATION_EVIDENCE`, not NEXY production proof.

## Claims proved locally
- E1: `src/uis.py` compiles under Python 3.13.5.
- E2: 10 unit/negative tests pass.
- E2 exhaustive influence check: all 16 Boolean influence masks over four binary variables were checked against exact declarative rule tables; the reported material-unknown set matched the independent expected mask.
- E3-local: root integration smoke imports UIS and executes a representative stable/materiality analysis.

## Negative / boundary paths covered
- duplicate variables/rules;
- values outside declared domains;
- unknown known-binding IDs;
- conflicting rule outputs;
- enumeration cap exceeded;
- domain canonical duplicate rejection;
- deterministic report fingerprint.

## Exact local commands
```text
python3 -m compileall -q .
python3 -m unittest discover -s 05-unknown-impact-slicer/tests -p 'test_*.py'
python3 integration_smoke.py
python3 deep_validation.py
```

## Limitations
- Completeness is relative to the declared finite domains and rules.
- A stable output does not convert unknown values into known facts and does not itself authorize execution.
- Large domains intentionally freeze at the configured state cap.
- No live NEXY ambiguity/clarification integration is claimed.
