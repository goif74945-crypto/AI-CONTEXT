# QUEUEBOUND-64 Design

**Status:** Lo4 AI proposal only.

## Objective
Compute a conservative worst-case fluid backlog bound and compare it with an explicit buffer/memory cap.

## Law
For `alpha(t)=b+r*t` served by `beta(t)=R*[t-T]+` with `R>=r`, use `B=b+rT`. Q64 multiplication is rounded upward. If `R<r`, a finite bound is not certified and the engine returns `FREEZE`.

## Failure behavior
Negative quantities, zero service rate, signed-128 overflow, or an unstable envelope never become PASS.
