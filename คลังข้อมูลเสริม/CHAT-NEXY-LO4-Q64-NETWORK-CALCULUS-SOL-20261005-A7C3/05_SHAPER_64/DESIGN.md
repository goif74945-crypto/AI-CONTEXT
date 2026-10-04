# SHAPER-64 Design

**Status:** Lo4 AI proposal only.

## Objective
Produce a stricter arrival envelope that can satisfy explicit backlog/deadline targets without weakening the service contract.

## Procedure
1. cap offered rate at service rate;
2. if a backlog limit exists, derive a maximum sustainable rate for service latency;
3. derive burst caps from backlog slack and deadline slack;
4. choose the most conservative legal burst cap;
5. independently re-run FLOWGUARD-64 on the synthesized envelope.

## Verdicts
- `UNCHANGED`: no shaping needed;
- `SHAPED`: a lower rate/burst is certified;
- `BLOCKED`: targets leave no positive sustained rate;
- `IMPOSSIBLE`: e.g. deadline is below intrinsic service latency or synthesis cannot certify itself;
- `FREEZE`: malformed/overflowing input.

No synthesized result is automatically applied to NEXY.
