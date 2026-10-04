# Integration Proposal

> **AI-PROPOSED / FUTURE INTEGRATION IDEA — NOT IMPLEMENTED IN NEXY.AI**

A future NEXY integration could run IX-Lab at three boundaries:

1. **Design-time**: score interaction flows before UI implementation.
2. **Run planning**: estimate expected human touches before a multi-agent task begins.
3. **Post-run telemetry**: compare planned vs observed interaction cost without storing sensitive message content.

## Proposed product behaviors

- Batch independent required questions into one interruption when semantics permit.
- Avoid confirmations for reversible, preauthorized low-risk actions.
- Require explicit confirmation for irreversible actions unless the user has provided valid preauthorization under governing law.
- Convert long dependency waits into background progress when execution semantics permit.
- Use progressive disclosure when choice entropy is high.
- Preserve explicit freeze states when authority or required evidence is unresolved.

## Guardrail

“Reduce friction” must never mean “skip safety, authority, or evidence.” IX-Lab therefore treats protected confirmations and freeze states as non-removable constraints.
