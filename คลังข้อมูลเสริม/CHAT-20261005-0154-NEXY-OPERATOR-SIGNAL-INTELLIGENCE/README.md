# NEXY Operator Signal Intelligence Lab

**AI-PROPOSED auxiliary reference project. Not current NEXY specification or production implementation.**

This lab explores five operator-signal systems intended to make a NEXY-compatible control surface quieter, clearer, and harder to accidentally silence:

1. Salience Gate
2. Interruption Governor
3. Milestone Compressor
4. Outcome Delta Compiler
5. Acknowledgement Debt Ledger

The core is deterministic, dependency-free Python 3.11+, uses canonical JSON/SHA-256 identities, and contains no model/network execution.

## Run tests
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## CLI
```bash
PYTHONPATH=src python -m nexy_signal_intelligence classify --input examples/signal_freeze.json
PYTHONPATH=src python -m nexy_signal_intelligence delta --input examples/outcome_delta.json
PYTHONPATH=src python -m nexy_signal_intelligence debt --input examples/debt.json
```

See `08_VALIDATION_REPORT.md` for evidence and limits.
