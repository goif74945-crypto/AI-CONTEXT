# Capability Degradation Ladder
Status: PROPOSAL

## Problem
Agents often improvise when a tool, credential, network, model feature or verifier disappears. Improvisation can silently weaken guarantees.

## Principle
Degradation must be specified by capability and evidence class. “Best effort” is not a universal fallback.

## Levels
D0 FULL: all required capabilities/evidence available.
D1 REDUNDANT_PATH: equivalent authorized verifier/tool available with same evidence class.
D2 REDUCED_NONCRITICAL: optional capability missing; required guarantees unaffected.
D3 READ_ONLY: mutation unavailable/unsafe; inspection may continue.
D4 ANALYSIS_ONLY: repository/runtime proof unavailable; produce hypotheses, never implementation PASS.
D5 FREEZE: missing capability prevents a unique safe/correct result.
D6 EMERGENCY_STOP: active risk or authority violation; cancel queued mutations where possible.

## Transition contract
Every downgrade records:
trigger, missing capability, affected requirements, lost evidence class, allowed actions, forbidden claims, recovery condition.

## Examples
- Browser E2E unavailable: UI runtime claim cannot PASS from static inspection.
- GitHub write unavailable: prepare patch/advice only; never claim repo changed.
- External authority unavailable: retain UNKNOWN, do not replace with model memory.
- Primary verifier broken but formally equivalent independent verifier exists: D1 only if equivalence itself is established.
- Context budget pressure: compress advisory context before authoritative requirements.

## Recovery
Upgrade only after capability is restored AND any stale work is revalidated. Restoring a tool does not retroactively validate outputs created while degraded.

## Acceptance
A test harness should deliberately remove one capability at a time and assert that forbidden completion claims never appear.
