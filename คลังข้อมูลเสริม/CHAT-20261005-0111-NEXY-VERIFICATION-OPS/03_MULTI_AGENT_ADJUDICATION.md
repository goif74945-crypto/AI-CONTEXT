# Multi-Agent Adjudication Contract

More agents do not automatically create more truth. Correlated models can agree on the same error.

## Roles
PROPOSER produces candidate. CHALLENGER searches for falsifiers and missing constraints. EVIDENCE_AUDITOR checks provenance and evidence-class fit. CONSTRAINT_AUDITOR checks User Law, scope, invariants and protected resources. JUDGE chooses only among evidence-supported candidates or freezes.

## Independence rules
- Challenger receives requirements and candidate, not hidden rationale.
- Evidence auditor validates sources directly where possible.
- Agreement count is not confidence unless failure correlation is understood.
- Judge must be able to return FREEZE.
- No agent self-certifies its own critical evidence.

## PASS rule
All critical requirements mapped; no critical constraint violation; required evidence fresh; contradictions resolved by authority/evidence; residual risk within explicit policy. Otherwise FREEZE with exact missing evidence or conflict.

Useful diversity means different failure detectors, validators, data sources, test methods or threat models. Merely changing model names is weak diversity.
