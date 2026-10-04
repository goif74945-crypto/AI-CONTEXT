# Action Visibility and Authority Boundary

**Classification:** AI-PROPOSED presentation matrix; backend authorization remains canonical.

## Core rule
`visible action != authorized action != executed action`

The Trust Card may suggest what the interface can expose. Every mutation request still goes through canonical backend auth, law, state guards, rate limits, and audit.

## Proposal matrix

| Condition | OWNER | OPERATOR | AUDITOR | PUBLIC_USER |
|---|---|---|---|---|
| READY | New Directive | New Directive | View System | View System |
| RESULT | View Result / Export | View Result / Export | View Result / Export | View Result |
| FREEZE recoverable | Recover + View Trace | View Trace | View Trace | View Trace |
| FREEZE non-recoverable | View Trace | View Trace | View Trace | View Trace |
| STOP | View Trace | View Trace | View Trace | View Trace |
| PENDING | Inspect Run | Inspect Run | Inspect Run | Inspect Run |
| HOLD | View Trace | View Trace | View Trace | View Trace |

## Dangerous action law
The only mutation-like action emitted by the current reference implementation for an incident is `Recover`, and it is:
- shown only to OWNER;
- shown only when backend freeze metadata says recoverable=true;
- marked `requires_backend_authorization=true`;
- marked `requires_confirmation=true`.

This is still not permission. Server-side checks remain mandatory.

## Why no automatic retry
Automatic retry can mask a deterministic failure, duplicate side effects, or turn a blocked state into probabilistic behavior. This reference therefore exposes inspect/recover semantics rather than a generic Retry button.
