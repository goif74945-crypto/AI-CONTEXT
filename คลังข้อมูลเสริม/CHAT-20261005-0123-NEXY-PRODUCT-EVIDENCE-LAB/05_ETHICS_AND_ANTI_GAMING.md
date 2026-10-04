# 05 — Ethics, Safety, and Metric-Gaming Controls

## Principle

A metric can be numerically improved while the user experience becomes worse. NPEL therefore treats the primary metric as necessary but not sufficient evidence.

## Prohibited risk flags in the reference compiler

- `dark_pattern`
- `coercion`
- `deception_without_consent`
- `privacy_violation`
- `safety_bypass`
- `security_bypass`

These are explicit structural blockers, not a complete ethics framework.

## Guardrail semantics

Every proposal must define at least one guardrail. A guardrail has:
- metric direction;
- baseline;
- maximum tolerated absolute degradation.

If observed degradation crosses that explicit hard threshold, evaluation freezes even when the primary metric appears successful.

## Anti-peeking note

This prototype assumes one declared terminal analysis. It does not implement sequential testing corrections. Repeated peeking can inflate false positives, so production adoption would require an alpha-spending, group-sequential, always-valid, or Bayesian design chosen explicitly.

## Human authority

NPEL reports evidence state only. It never returns an automatic shipping decision. Every evaluation result contains `human_decision_required=true`.
