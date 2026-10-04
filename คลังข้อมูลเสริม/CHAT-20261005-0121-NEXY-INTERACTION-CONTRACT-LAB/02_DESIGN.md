# Design: Interaction Contract Retention Engine

Status: **AI-PROPOSED CONCEPT WITH REFERENCE IMPLEMENTATION**

## Problem
A capable agent can obey many rules individually yet still lose the user’s actual contract over a long workflow. Common failure modes include re-asking facts already supplied, acting outside delegated scope, relying on unstated assumptions, and declaring completion before every mandatory directive has proof.

This lab treats that as an explicit data problem rather than a vague “conversation quality” problem.

## Contract model

### Directive
A user/system requirement represented by:
- stable ID;
- human text;
- kind (`requirement`, `constraint`, `forbidden`, `preference`, `acceptance`);
- criticality;
- related scopes;
- explicit conflicts;
- resolved/unresolved state.

### Event
An ordered event represented by:
- sequence number;
- actor;
- type (`clarification`, `action`, `evidence`, `completion`, `note`);
- referenced directives;
- touched scopes;
- explicit assumptions;
- evidence outcome/reference;
- completion status.

## Determinism boundary
The reference implementation deliberately does not perform NLP, embeddings, model calls, web calls, clock access, random access, filesystem mutation, or hidden I/O inside analysis. Given the same parsed JSON object, it produces the same report.

Semantic extraction from raw chat could be a separate upstream AI worker, but its output must be treated as candidate structure requiring validation. This lab does not pretend candidate extraction is truth.

## Core invariants
1. Protected scope touch is always critical.
2. Unknown scope on an action is unauthorized unless explicitly granted.
3. Mandatory directives cannot be considered complete without effective `pass` evidence.
4. A `pass` with no evidence reference is suspicious and penalized.
5. Explicit conflicting active directives block completion.
6. Re-clarifying a resolved directive is interaction debt.
7. Action assumptions are visible, never hidden.
8. A completion claim is blocked while mandatory directives are not PASS.

## Complexity
For D directives and E events, analysis is approximately O(D + E + explicit-conflict-edges). No global semantic search is performed.

## Trade-offs
- **Pro:** predictable, auditable, model-independent.
- **Pro:** useful for regression testing agent workflows.
- **Con:** requires structured input.
- **Con:** cannot discover implicit conflict in prose.
- **Con:** scoring weights are policy knobs, not universal truth.

## Safe future integration shape
If ever adopted, keep this as an admission/check layer around an agent workflow rather than as a truth oracle. The NEXY authority layer would decide whether findings should freeze execution.
