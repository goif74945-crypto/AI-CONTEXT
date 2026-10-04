# Fault Injection Matrix

Principle: inject one controlled fault at a time first; compound faults only after single-fault behavior is understood.

FI-001 malformed framing -> reject; never heuristic repair into authority.
FI-002 ambiguous intent -> reject/freeze; never arbitrary choice.
FI-003 missing constraint -> reject; never permissive default.
FI-004 DAG cycle -> failsafe/freeze; never truncate cycle.
FI-005 verifier disagreement -> freeze; never majority shortcut.
FI-006 agent timeout -> bounded failure; never implicit yes vote.
FI-007 duplicate proposal -> de-duplicate; never quorum inflation.
FI-008 evidence alias -> count once; never evidence inflation.
FI-009 evidence mutation -> reject; never trust stale verified label.
FI-010 state corruption -> freeze; never unaudited auto-correct.
FI-011 stale release token -> reject.
FI-012 clock rollback -> must not resurrect expired authority.
FI-013 disk full during evidence write -> fail closed.
FI-014 kill before commit -> no partial authoritative result.
FI-015 kill after commit -> replay without duplicate side effect.
FI-016 dependency drift -> replay identity mismatch.
FI-017 config mutation -> invalidate/re-evaluate authorization.
FI-018 signature corruption -> reject.
FI-019 unknown freeze reason -> NOT VERIFIED, never assume recoverable.
FI-020 unauthorized recovery -> deny.

Compound campaigns: timeout+disk pressure; stale token+recovery; duplicate evidence+correlated agents; clock skew+restart; law drift+replay; verifier crash+consensus pressure.

Every run records seed, exact injection event, state before/after, output visibility, authoritative evidence references, and cleanup.
