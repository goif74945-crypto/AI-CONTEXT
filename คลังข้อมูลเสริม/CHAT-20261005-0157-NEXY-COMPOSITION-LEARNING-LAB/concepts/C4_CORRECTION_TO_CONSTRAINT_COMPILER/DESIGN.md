# C4 — Correction-to-Constraint Compiler (CCC)

> **AI_PROPOSED_CONCEPT / NON-CANONICAL**

## Objective
Turn an explicit, verified correction into a deterministic regression contract while preventing a local correction from silently becoming a global rule.

## Design choice: no free-text authority
This prototype does not parse natural language into law. An upstream model may *propose* a structured correction, but promotion requires explicit fields. This keeps AI generation separate from authority.

## Scope modes
### BOUNDED
Requires at least two exact selector dimensions and forbids wildcard/null selector values. Example: project + operation.

### GLOBAL_EXPLICIT
Requires:
- authority exactly `USER_LAW`;
- selector exactly `{ "global": true }`.

This is intentionally inconvenient. Global rules should be hard to create accidentally.

## Assertions
Supported deterministic operators:
- `eq`, `neq`
- `contains`, `not_contains`
- `exists`, `not_exists`

Nested output fields use dot paths.

## Conflict handling
Within an identical scope/selector, the compiler freezes on proven direct conflicts including:
- different equalities for the same field;
- `eq(v)` vs `neq(v)`;
- `exists` vs `not_exists`;
- an existence-requiring rule vs `not_exists`;
- `contains(v)` vs `not_contains(v)`.

The conflict detector is intentionally conservative and does not pretend to solve arbitrary semantic contradictions.

## Why NEXY could benefit
Human corrections are valuable, but naive “learning” can poison future behavior by overgeneralizing one case. CCC provides a narrow bridge from correction → explicit scope → regression assertion, preserving human authority without uncontrolled memory learning.

## Code / tests
- Code: `src/nexy_aux/corrections.py`
- Tests: `tests/test_corrections.py`, `tests/test_properties.py`, `tests/test_hardening.py`
