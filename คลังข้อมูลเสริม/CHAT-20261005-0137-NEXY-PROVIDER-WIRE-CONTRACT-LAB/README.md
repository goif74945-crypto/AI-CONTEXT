# NEXY Provider Wire Contract Lab

**Status: AI-PROPOSED supplemental engineering artifact. Not a current NEXY requirement.**

This project is a standalone reference implementation for a deterministic, fail-closed canonical event boundary between provider-specific AI streams and NEXY-facing orchestration.

It is designed to support NEXY's documented provider/model hot-swap direction without allowing provider-specific wire behavior to become CORE semantics.

## Run

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Core modules
- `model.py` immutable canonical event model
- `codec.py` deterministic JSON and SHA-256 helpers
- `state.py` sequence/message/tool/terminal state validation
- `replay.py` deterministic transcript hash chain
- `boundary.py` fail-closed NEXY-facing result

## Evidence boundary
This repository package can prove canonical-contract behavior in isolation. It does **not** prove live compatibility with any provider or live NEXY runtime until provider-specific adapters and integration tests exist.
