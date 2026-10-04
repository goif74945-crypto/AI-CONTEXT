# Architecture

> **AI-PROPOSED CONCEPT — NOT CURRENT NEXY SPEC**

```text
InteractionPlan JSON
      |
      v
  model.py  ---- validation / identity / explicit fields
      |
      +--> scorer.py ---- metrics + invariant findings + budget gates
      |
      +--> optimizer.py - safe transformations + advisory suggestions

DecisionContext JSON
      |
      v
  planner.py ---- deterministic EXECUTE / ASK / CONFIRM / FREEZE

cli.py ---- stable machine-readable interface
```

## Authority

The tool never decides what NEXY law *is*. Callers supply explicit state such as `authority_conflict`, `missing_required_information`, `evidence_required`, and `evidence_sufficient`. The planner only applies published deterministic precedence.

## Interaction cost model

The score is intentionally interpretable rather than learned:

`12*touches + 10*blocking + 5*choice_bits + 7*context_switches + wait_penalty + 2*effort + 8*freeze_steps`, clamped to `[0,100]`.

This is a research heuristic, not a canonical NEXY threshold. Budgets are configurable and must be calibrated with product research before any production adoption.

## Failure semantics

- malformed input: explicit validation error;
- duplicate step identity: reject;
- unknown kind: reject;
- missing guarded target: structural finding;
- ambiguous high-impact decision state: freeze via explicit flags, never infer authority;
- optimizer uncertainty: suggestion only, no mutation.
