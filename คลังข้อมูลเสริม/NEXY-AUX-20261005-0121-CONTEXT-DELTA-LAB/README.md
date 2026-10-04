# NEXY Context Delta Lab

**Status: AI-PROPOSED / AUXILIARY / NON-CANONICAL**

This project is an isolated tool prototype stored in `AI-CONTEXT`. It does not modify NEXY.AI and does not promote any requirement into NEXY.AI scope.

## Purpose
When project law, build specifications, product design, or deployment evidence evolves, old verification can silently become stale. Context Delta Lab turns two normalized snapshots into a deterministic change/impact report.

It answers five questions:
1. Which requirement records changed?
2. What kind of change occurred?
3. Which dependent records are transitively impacted?
4. What evidence class should be rerun or reviewed?
5. In what deterministic order should revalidation happen?

It deliberately does **not** answer whether NEXY.AI is implemented, correct, deployed, or safe.

## Core invariants
- Same valid input bytes produce the same canonical report content.
- Unknown authority/scope/evidence classes are rejected rather than guessed.
- Duplicate IDs, missing dependencies, and dependency cycles freeze processing.
- Impact propagation is closed-world and deterministic.
- A report never upgrades implementation status. Impacted records are `NOT_VERIFIED` until matching evidence exists.
- Current governing/build authority changes outrank advisory changes.

## Quick run
```bash
python -m context_delta_lab.cli fixtures/base.json fixtures/current.json --output report.json
```
Use `PYTHONPATH=src` from this project directory.

## Verify
```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m py_compile src/context_delta_lab/*.py tests/*.py
```

## Exit codes
- `0`: valid inputs and report produced.
- `2`: semantic validation failed; processing froze.
- `3`: I/O or JSON decoding failed.
- `4`: `--fail-on-change` was requested and at least one delta exists.

## Authority
This prototype is advisory only. Canonical NEXY source authority remains governed by the project hierarchy in `AI-CONTEXT`.
