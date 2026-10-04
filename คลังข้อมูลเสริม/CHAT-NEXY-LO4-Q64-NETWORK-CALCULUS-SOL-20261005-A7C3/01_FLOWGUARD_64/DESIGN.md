# FLOWGUARD-64 Design

**Status:** Lo4 AI proposal only.

## Objective
Fail closed before admitting a declared arrival envelope into a declared service envelope when finite deterministic bounds cannot be established.

## Inputs
- token-bucket burst `b >= 0`;
- arrival rate `r >= 0`;
- service rate `R > 0`;
- service latency `T >= 0`;
- optional backlog/deadline limits.

## Law
`R < r` is not stable under this model and returns `REJECT`. Otherwise compute conservative backlog and delay bounds. Optional limits can also produce `REJECT`. Malformed/overflowing contracts produce `FREEZE`.

## Integration posture
Advisory pre-admission certificate only. It cannot enqueue, release, promote, or change LAW.
