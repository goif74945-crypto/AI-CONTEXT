# Architecture Contracts
Component contract: responsibility; owned state; inputs/outputs; dependencies; authority; failure modes; retry semantics; timeout budget; observability; retention; compatibility.
Dependency contract: sync/async; required/optional; degradation; circuit break; latency budget; stale policy; consistency; ownership.
State machine: legal states/transitions; preconditions; authorized actor; idempotency; compensation; terminal/impossible states.
Invariants: no hidden writes; downstream acceptance never grants authority; server enforces auth; cache is not truth unless explicit; retries cannot duplicate irreversible effects; finite timeouts; optional dependencies degrade explicitly.
Review: source of truth, mutation owner, concurrency, partial failure, duplicate/delayed/reordered events, crash recovery, forged authority, stale unsafe mutation, transition evidence, rollback.
