# 03 — INTERACTION FRICTION BUDGET

## Goal

Minimize user round-trips without turning “autonomy” into permission to guess.

## Model

Define:

- `C` = number of clarification turns;
- `R` = repeated clarification count;
- `M` = unresolved material unknown count;
- `A` = authority risk indicator;
- `I` = impact class;
- `V` = reversibility class.

The budget is **not** a scalar permission score. It is a UX diagnostic layered below hard correctness gates.

### Proposed advisory cost

`F = wC*C + wR*R`

where `wR > wC`, because asking a previously answered question is usually more damaging than asking a new necessary question.

However:

`M > 0 OR A = conflict OR required_safety_check = true`

cannot be overridden by `F`.

## Practical rules

1. Reuse already resolved values from the current scoped intent state.
2. Batch independent low-risk clarifications when possible.
3. Prefer reversible read-only progress when missing facts do not affect correctness.
4. Ask before irreversible/high-impact state mutation if authority is unresolved.
5. When a prior answer becomes stale due to changed evidence, asking again is not counted as an unjustified repeat, but the new evidence must be recorded.
6. Do not hide the reason for a mandatory clarification behind generic wording.

## Metrics for future experiments

- clarification turns per completed objective;
- repeated-question rate;
- user correction rate after autonomous proceed;
- freeze precision for authority conflicts;
- material-unknown escape rate (target: zero);
- successful reversible progress before first clarification;
- cross-model decision consistency.

No target numbers are canonical in this proposal.
