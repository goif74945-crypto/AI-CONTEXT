# Lo4 Q64.64 Deterministic Control Plane Architecture

## Layering
`NEXY adapter (future, outside scope) -> 20 pure decision modules -> shared checked Q64.64 kernel`

## Numeric contract
- signed 128-bit raw domain
- 64 integer/sign bits + 64 fractional bits
- checked overflow
- round-to-nearest-even for mul/div/ratio conversion
- exact BigInt state and deterministic lexical tie-breaks

## Why this exists
NEXY has broad governance/evidence/control architecture. This lab adds a reusable deterministic numeric substrate for decisions that would otherwise drift across platforms when implemented with IEEE-754 floats.

## Promotion boundary
These modules are Lo4 proposals. Even a full local test pass only establishes this lab's local implementation evidence. It does not make them Canon, does not prove NEXY integration, and does not prove deployment.
