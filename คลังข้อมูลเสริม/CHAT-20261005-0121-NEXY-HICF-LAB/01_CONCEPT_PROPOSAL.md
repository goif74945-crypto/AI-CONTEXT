# 01 — AI-PROPOSED CONCEPT: HUMAN INTENT CONTINUITY FABRIC

## Status

AI-PROPOSED. This file is an engineering proposal, not NEXY law, not a current implementation claim, and not a request to mutate the NEXY.AI repository.

## Core hypothesis

NEXY already defines authority, intent resolution, freeze semantics, verified output, UI truth separation, and user control. A complementary missing layer is a deterministic **continuity contract** between conversational interaction and deeper control layers.

The continuity contract should answer five questions before an agent continues work:

1. Is this still the same objective?
2. Did any immutable user constraint change?
3. Is a missing fact actually material to the next action?
4. Has this question already been answered?
5. Is the proposed action reversible and authorized enough to proceed without another round-trip?

## Proposed value

### User value
- fewer pointless clarification loops;
- fewer accidental scope drifts;
- fewer “I already told you that” failures;
- clearer reasons when the system must stop;
- consistent behavior across different AI workers/providers;
- explicit boundaries around inferred preferences.

### System value
- deterministic interaction decisions;
- replayable intent state;
- measurable clarification quality;
- machine-readable handoff between DIALOG/CIRL and deeper control layers;
- reduced coupling between UX smoothness and authority/safety decisions.

## Key law

> Interaction efficiency may reduce unnecessary questions, but it may never reduce required authority, safety, or correctness checks.

Formally:

`UX_FRICTION_OPTIMIZATION < USER_AUTHORITY < REQUIRED_CORRECTNESS_AND_SAFETY`

This ordering is a proposal for HICF behavior and must not be confused with a new canonical NEXY authority hierarchy.

## Why this is distinct from existing supplementary work

The inspected supplementary inventory already contains extensive work on evidence, verification economics, semantic contracts, counterfactual safety, replay, resilience, knowledge decay, capacity economics, and release proof. Path-level search found no existing named subsystem for:

- human intent continuity;
- interaction friction budgeting;
- clarification gating;
- preference scope enforcement.

This lab therefore targets a user-interaction/control gap rather than repeating proof/reliability material.
