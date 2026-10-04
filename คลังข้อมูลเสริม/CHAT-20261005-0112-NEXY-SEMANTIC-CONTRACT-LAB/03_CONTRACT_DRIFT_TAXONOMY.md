# Contract Drift Taxonomy

Contract drift is any divergence between authorized meaning and executed/claimed meaning.

## CD-01 Objective Drift
Agent optimizes an attractive proxy instead of the requested end state.
Detection: compare deliverable acceptance criteria to final artifact.

## CD-02 Scope Inflation
Agent adds redesigns, refactors, integrations, or cleanup not required.
Signal: action has no REQ/VAL trace.

## CD-03 Scope Erosion
Difficult requirements disappear from the plan.
Signal: mandatory clauses have no terminal state.

## CD-04 Authority Inversion
A summary, model guess, stale doc, or external source overrides authoritative project material.

## CD-05 Unknown Collapse
Missing data is filled with plausible values.
This is one of the most dangerous AI-specific drifts because output can look polished.

## CD-06 Identity Drift
Correct operation applied to wrong repo, branch, file, account, environment, tenant, user, or record.

## CD-07 Temporal Drift
Previously true evidence is treated as current after mutable state changed.

## CD-08 Interface Drift
Implementation remains locally correct while violating API/schema/event/storage contract.

## CD-09 Verification Drift
Tests prove a different property than the requirement.
Example: HTTP 200 is treated as proof that persisted business state is correct.

## CD-10 Evidence Drift
Evidence exists but does not support the exact completion claim.

## CD-11 Recovery Drift
A fix changes additional surfaces and creates secondary failures.

## CD-12 Retry Drift
A repeated action is assumed safe despite non-idempotent side effects.

## CD-13 Summary Compression Drift
Long context is compressed and exceptions, negatives, units, qualifiers, or precedence rules vanish.

## CD-14 Tool Semantics Drift
Agent assumes a tool action has semantics it does not guarantee, such as assuming "request accepted" means "state committed."

## CD-15 Completion Drift
Agent equates effort, tool success, or artifact creation with objective completion.

## Severity
S0 cosmetic: no semantic effect.
S1 localized: recoverable, non-critical mismatch.
S2 material: requirement violated but bounded.
S3 critical: security/data/authority/irreversible or major objective failure.
S4 catastrophic: broad destructive mutation, secret exposure, or systemic false completion.

## Triage
For S2+: freeze related writes, preserve evidence, identify last verified state, perform smallest safe correction, then re-run affected contract checks.
