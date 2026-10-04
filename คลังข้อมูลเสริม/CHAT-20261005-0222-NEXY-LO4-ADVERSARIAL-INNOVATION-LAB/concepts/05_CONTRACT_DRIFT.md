# CONTRACT-DRIFT — Task Contract Drift Budgeter

Status: `Lo4_AI_PROPOSAL_ONLY`

## Problem
Long autonomous work can start with a strict contract and gradually become easier by silently expanding scope, removing invariants, weakening forbidden actions, adding assumptions or dropping evidence requirements.

## Mechanism
Compare normalized structured Task Contract snapshots and emit deterministic drift events:
- scope expansion;
- scope narrowing;
- success-invariant removal;
- forbidden-action removal;
- assumption injection;
- required-evidence removal.

Dangerous unapproved events freeze by default. Explicit approval can target a specific event ID. Remaining non-approved drift consumes a configured budget.

## Invariants
- dangerous weakening cannot silently pass;
- approval is event-specific rather than blanket;
- cost and reasons are deterministic for normalized inputs;
- approval authority itself remains external and must be authenticated by a future integration.

## NEXY value
Turns scope fidelity into a continuously checkable invariant during long execution rather than a one-time planning promise.
