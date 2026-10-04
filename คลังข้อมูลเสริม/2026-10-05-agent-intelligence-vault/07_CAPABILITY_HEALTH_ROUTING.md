# Capability Health Routing
Represent each capability with supported operations, authority, health, latency, cost, freshness, determinism, privacy constraints, and known failure modes.
Health states: HEALTHY, DEGRADED, UNAVAILABLE, UNAUTHORIZED, STALE, UNKNOWN.
Routing should satisfy task requirements first, then optimize cost/latency.
Fallbacks must preserve semantics. A web search is not automatically equivalent to an authoritative connected source; a draft is not equivalent to a completed mutation.
If no fallback satisfies acceptance criteria, report BLOCKED or NOT VERIFIED rather than fabricating equivalence.
