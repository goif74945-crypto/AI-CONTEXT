# Temporal Truth Engine
Truth in production systems has a time dimension. Store confidence and freshness separately.
Suggested freshness classes: IMMUTABLE, SLOW, MODERATE, FAST, REALTIME.
Claim record: statement, source, observed_at, valid_from, optional valid_until, freshness_class, verification_status, contradiction_set.
Rules: stale high-confidence data is not current truth; realtime claims require realtime-capable evidence; conflicting temporal observations remain separate until resolved; last-known-good values must carry timestamps.
Useful future subsystem: temporal gates can reject evidence whose age exceeds the decision's freshness requirement.
