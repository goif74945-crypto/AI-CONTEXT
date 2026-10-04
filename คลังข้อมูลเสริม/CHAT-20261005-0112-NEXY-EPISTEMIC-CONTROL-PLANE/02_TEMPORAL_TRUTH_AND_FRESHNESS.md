# Temporal Truth & Freshness
Track four clocks separately: event_time, observation_time, ingestion_time, verification_time.
Freshness contract fields: max_age, refresh_trigger, invalidation_event, authoritative_refresh_source, stale_behavior (FREEZE/WARN/REVERIFY/ALLOW_READ_ONLY).
Derived claims cannot outlive the weakest applicable un-reverified dependency.
When time sensitivity affects correctness, missing freshness semantics is a verification gap.
Status: DESIGN PROPOSAL.