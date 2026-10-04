# NEXY Compatibility Boundary

## Read-only evidence pin
- repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

## Observed compatibility constraints
- LAW, not SWARM/AI, authorizes final release transitions.
- NEXY code already uses fixed-point/Q64 authority paths.
- NEXY NX v0.1 requires deterministic parsing/compilation, explicit failure, no hidden authority, no clock/random/fs/network/db/process/env access, signed 128-bit arithmetic, source bounds and sealed compiler results.
- UI/human/auxiliary outputs are requests/presentation rather than backend authority.

CourtScript mirrors these constraints instead of inventing a competing authority model.

## Proposed future adapter only
A future NEXY-owned adapter could receive an EPC policy artifact and exact source digest, recompile/verify it in isolation, map approved predicates to existing NEXY evidence/metric contracts, and return an advisory review packet to the authoritative process. It must never permit CourtScript to call CORE/JUDGE/LAW mutation APIs.

This adapter is **not implemented in NEXY.AI** by this work.
