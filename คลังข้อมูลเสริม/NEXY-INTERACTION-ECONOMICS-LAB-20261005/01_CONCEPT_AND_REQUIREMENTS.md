# Concept and Requirement Ledger

> **AI-PROPOSED CONCEPT — NOT CURRENT NEXY SPEC**

## Objective

Create a model-agnostic tool that makes user-facing interaction cost measurable without weakening NEXY's authority, safety, verification, or freeze semantics.

## Requirements

| ID | Requirement | Evidence target |
|---|---|---|
| IX-R01 | Parse a declarative interaction plan deterministically | E2 tests |
| IX-R02 | Measure human touches, blocking touches, choices, switches, wait, effort | E2 tests |
| IX-R03 | Detect irreversible actions without a valid guard | E2 tests |
| IX-R04 | Detect redundant confirmations | E2 tests |
| IX-R05 | Enforce configurable friction budgets | E2 tests |
| IX-R06 | Produce deterministic action routing from explicit authority/risk/evidence state | E2 tests |
| IX-R07 | Never auto-remove a law-required confirmation | E2 tests |
| IX-R08 | Provide safe-only optimization and separate non-mutating suggestions | E2 tests |
| IX-R09 | Expose JSON CLI for reproducible analysis | E3 subprocess test |
| IX-R10 | Remain dependency-light and model/provider independent | E1 import/compile + inspection |

## Acceptance criteria

- Python compilation passes.
- Full unit/integration suite passes.
- Example high-friction plan produces budget or structural findings.
- Decision example deterministically produces a documented action.
- No write to NEXY.AI repositories.
