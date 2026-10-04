# NEXY Interaction Economics Lab (IX-Lab)

> **STATUS: AI-PROPOSED CONCEPT / REFERENCE IMPLEMENTATION. NOT CURRENT NEXY SPEC.**

IX-Lab is a deterministic research tool for measuring the cost imposed on a human by an AI workflow while preserving human authority and NEXY-style freeze semantics. It is deliberately orthogonal to the existing assurance-heavy supplemental packs: its primary object is the **interaction surface**, not model intelligence, evidence architecture, or runtime security.

## Why this exists

A system can be safe and correct while still exhausting users with confirmations, repeated clarifications, needless waiting, excessive choices, and context switching. NEXY's current context says complexity should scale behind a small user-facing surface. IX-Lab makes that design principle measurable.

It analyzes a declarative interaction plan and reports:

- human touches and blocking touches;
- choice entropy (`log2` choice complexity);
- context switches;
- user-visible wait exposure;
- explicit effort;
- unguarded irreversible actions;
- redundant confirmations;
- budget violations;
- safe optimization opportunities.

It also includes an authority-preserving planner that deterministically chooses one of `EXECUTE`, `ASK_CLARIFICATION`, `CONFIRM`, or `FREEZE` from explicit state. No model inference is needed.

## Non-goals

This package does **not** modify NEXY.AI, prove NEXY runtime behavior, infer user preferences, silently relax User Law, or redefine NEXY requirements. It is a proposal and testbed only.

## Run

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m nexy_ixlab.cli analyze examples/high_friction_plan.json
PYTHONPATH=src python -m nexy_ixlab.cli decision examples/decision_context.json
```

## Core invariants

1. Material authority conflict => `FREEZE`.
2. Required material information missing => `ASK_CLARIFICATION`.
3. Non-preauthorized irreversible action => `CONFIRM`.
4. Required evidence unavailable => `FREEZE`.
5. Safe, reversible, authorized action with sufficient evidence => `EXECUTE`.
6. Automatic optimization may only remove a redundant confirmation when the guarded action is explicitly reversible or preauthorized and the confirmation is not required by law.
7. No hidden assumption converts ambiguity into authority.
