# Evidence — Epistemic Saturation Controller (ESC)

Truth class: `REFERENCE_IMPLEMENTATION_EVIDENCE`, not NEXY production proof.

## Claims proved locally
- E1: `src/esc.py` compiles under Python 3.13.5.
- E2: 9 unit/negative tests pass.
- E2 structural cross-check: 24 independently computed novelty/saturation scenarios pass in `deep_validation.py`.
- E3-local: root integration smoke imports ESC and executes a representative multi-round saturation path.

## Negative / boundary paths covered
- duplicate round IDs;
- duplicate agent IDs within one round;
- invalid patience/minimum-round settings;
- repeated claim/evidence/domain support contributing zero novelty;
- independent-domain support counted separately;
- saturation explicitly not treated as release permission.

## Exact local commands
```text
python3 -m compileall -q .
python3 -m unittest discover -s 03-epistemic-saturation-controller/tests -p 'test_*.py'
python3 integration_smoke.py
python3 deep_validation.py
```

## Limitations
- Claim identity and independence-domain identity are declared upstream; ESC does not semantically deduplicate natural language.
- `SATURATED` means no declared structural novelty for the configured patience window, not correctness or consensus.
- No live NEXY swarm integration is claimed.
