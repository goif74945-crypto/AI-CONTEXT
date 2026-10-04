# NEXY Truth Surface Compiler (NXTS)

> **STATUS: AI-PROPOSED CONCEPT + EXECUTABLE REFERENCE PROTOTYPE. ADVISORY ONLY.**  
> This project is not canonical NEXY law, is not part of the NEXY.AI implementation repository, and does not authorize any release/deployment behavior.

## Why this exists
NEXY's project context repeatedly separates a large controlled backbone from a small user-facing surface and requires one legal verified output or freeze. That creates a practical product problem: internal truth can be rich, but the user should not have to read orchestration traces, provider details, secret-bearing metadata, or a hundred-line proof graph.

NXTS explores a deterministic boundary that compiles internal claim records into a **Result Capsule**:

`internal claims + materiality + visibility + evidence refs → RELEASE/FREEZE + minimal public facts + uncertainties + receipt`

The core design goal is **truth preservation under UX compression**.

## Prototype guarantees
The reference code currently proves only what its tests cover:

- deterministic sorting and canonical SHA-256 receipts;
- fail-closed handling of unknown claim statuses;
- freeze on material `UNKNOWN`, `CONFLICT`, or `NOT_VERIFIED`;
- freeze when a material fact has no evidence reference;
- public/internal/sensitive visibility separation;
- narrow token-pattern redaction for common API/JWT forms;
- order-invariant compilation for semantically identical claim sets;
- CLI exit code `0` for RELEASE, `2` for FREEZE, `64` for malformed input.

It does **not** prove production security, complete secret detection, semantic truth of evidence refs, or compatibility with the live NEXY codebase.

## Run

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m nxts.cli fixtures/release.json --pretty
PYTHONPATH=src python -m nxts.cli fixtures/freeze-unknown.json --pretty
```

## Integration concept
Treat NXTS as a possible future adapter **after** NEXY's authoritative judge/verification layers and **before** the human-facing result surface. It must never become a second authority layer. It formats truth classes; it does not decide whether evidence is genuinely valid.
