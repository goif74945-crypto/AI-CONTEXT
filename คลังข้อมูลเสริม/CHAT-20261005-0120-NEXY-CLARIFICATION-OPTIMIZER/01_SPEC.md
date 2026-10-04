# NEXY Clarification Optimizer (NCO) v1 — AI Proposal

Status: AI_PROPOSAL / REFERENCE_IMPLEMENTATION / NOT_CURRENT_NEXY_REQUIREMENT

## Objective
Given already-detected unresolved variables and a finite catalog of authorized clarification questions, return the deterministic minimum-burden question set that covers every blocking variable, or return an explicit BLOCKED result with proof of what cannot be resolved.

## Non-goals
- Natural-language intent inference.
- Guessing missing answers.
- Rewriting user intent.
- Deciding upstream authority.
- Mutating NEXY.AI or any canonical NEXY contract.
- Probabilistic personalization.

## Inputs
Unknown:
- id: stable identifier
- blocking: whether the unknown prevents legal release
- description: audit text

Question:
- id: stable identifier
- text: user-facing prompt text
- resolves: non-empty set of Unknown ids
- cost: positive integer attention cost

Problem:
- unknowns
- questions
- optional max_total_cost

## Output states
READY: no blocking unknown remains.
ASK: a complete legal clarification cover exists within budget.
BLOCKED: at least one blocking unknown has no resolver, or the exact minimum cover exceeds budget.

## Optimization order
Among complete covers, minimize lexicographically:
1. total cost
2. number of questions
3. sorted question-id tuple

## Validation
Reject malformed input before optimization:
- duplicate unknown or question ids
- blank ids/text/descriptions
- question with zero resolved unknowns
- question referencing unknown ids absent from the problem
- non-positive question cost
- negative max_total_cost

## Determinism
Equivalent problems that differ only in input ordering must produce identical status, selected question ids, cost, coverage proof, and canonical fingerprint.

## Proof obligations
ASK must include a coverage witness for every blocking unknown.
BLOCKED(uncovered) must list every blocking unknown with no available resolver.
BLOCKED(budget) must report exact minimum required cost and the selected minimum cover candidate.
READY must select nothing and cost zero.

## Algorithm
Exact branch-and-bound weighted set cover over blocking unknowns. Questions that resolve no blocking unknown are excluded from the search. Search order and tie-breaking are canonicalized.

## Safety invariant
NCO only selects questions. It never supplies answers and never converts UNKNOWN to known state.

## Integration boundary
This proposal is a possible upstream companion to NEXY::DIALOG / USER_INTENT_TRACK after ambiguity detection and before execution release. It is not authority and must not bypass CORE/JUDGE/LAW.
