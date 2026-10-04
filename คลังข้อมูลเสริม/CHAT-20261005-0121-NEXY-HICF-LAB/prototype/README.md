# HICF reference prototype

This prototype is intentionally dependency-light and non-production. It demonstrates deterministic control semantics, not integration with NEXY.AI.

## Run

```bash
python -m py_compile hicf.py test_hicf.py exhaustive_matrix.py
python -m unittest -v test_hicf.py
python exhaustive_matrix.py
```

## Expected proof class

- compile: E1
- unit tests: E2
- exhaustive matrix: E2-style model behavior validation

No E3+ claim is made.
