# NEXY User Leverage Fabric (NULF)

> **AI-PROPOSED / NON-GOVERNING / STANDALONE REFERENCE IMPLEMENTATION**
>
> This project does not modify NEXY.AI, is not part of the current 837-row NEXY build matrix, and is not evidence that NEXY currently implements these behaviors.

Work ID: `CHAT-20261005-0156-NEXY-USER-LEVERAGE-FABRIC`

## Why this project exists

The supplemental repository already contains many strong projects around proof, truth, privacy, concurrency, authority and model/tool conformance. This lab deliberately moves into five narrower “make the system more useful to a human without weakening control” gaps:

1. **Goal Contribution Graph** — reject work that cannot justify its contribution to acceptance criteria.
2. **Verified Capability Composer** — plan a policy-compliant typed capability chain without executing it.
3. **Artifact Consumer Fitness Gate** — reject outputs that are correct-looking but unusable by their intended consumer.
4. **Supply-Chain Trust Gate** — reject unpinned/untrusted/over-privileged dependencies before admission.
5. **Mastery Path Compiler** — build a prerequisite-respecting onboarding path from declared knowledge, never inferred competence.

## Run

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m nulf.demo
```

## Verified local state

At the evidence capture point:

- Python `3.13.5`;
- pytest `9.0.2`;
- compileall PASS;
- `31 passed`;
- integrated demo: five engines PASS;
- deterministic repeated demo SHA-256: `83560e83819e37695f043d831e5186feb4a0b44abdd235af3f4c4ec85d9dc35c`.

See `07_VALIDATION_REPORT.md` and `08_FINAL_AUDIT.md` for evidence boundaries. File presence alone is not proof.
