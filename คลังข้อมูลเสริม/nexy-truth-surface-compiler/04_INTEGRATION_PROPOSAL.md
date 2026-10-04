# Integration Proposal

## Classification
**AI-PROPOSED FUTURE INTEGRATION IDEA / DO NOT TREAT AS CURRENT BUILD REQUIREMENT**

## Placement hypothesis
If NEXY ever adopts an equivalent concept, the safest role is a **presentation adapter after authoritative verification/adjudication** and before the user-facing view. It must not be able to upgrade evidence state or authorize execution.

Conceptual placement only:

```text
... authoritative verification / judge ...
                ↓
         typed claim envelope
                ↓
      Truth Surface Compiler
                ↓
      NEXY::VIEW / FRONT surface
```

## Adoption gates
Do not integrate without all of:
1. mapping to current DOC-B/DOC-C authority;
2. exact schema ownership and versioning;
3. security review for secret leakage;
4. property/adversarial tests for truth-status preservation;
5. compatibility tests with freeze/error semantics;
6. UI usability testing showing the capsule is actually clearer;
7. exact-head regression evidence.

## Why this may help users
- concise but auditable results;
- explicit freeze reason instead of silent failure;
- less internal implementation noise;
- stable machine-readable output for UI, CLI, mobile, and accessibility surfaces;
- deterministic replay when users ask “why did this freeze?”
