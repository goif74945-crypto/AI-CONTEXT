# Production AI Observability
Trace: request/task correlation; model/config version; prompt/spec fingerprint; retrieval fingerprint; source IDs+versions; tool calls+latency+outcome class; claim/evidence links; validation outcome; resource metrics; final status.

Semantic metrics: grounded_claim_rate; unsupported_critical_claim_rate; retrieval_miss_rate; tool_false_success_detection_rate; requirement_coverage; verification_coverage; contradiction_rate; abstention_correctness; recovery_success_rate.
Operational: p50/p95/p99 latency; tool/dependency error rate; retries; context size; rate-limit events; queue age where applicable.

Privacy: redact secrets; minimize raw sensitive prompts when fingerprints suffice; retention by class; access-control traces; provenance may itself be sensitive.

High-severity alerts: cross-tenant leakage; unauthorized mutation; unsupported critical claim marked verified; provenance loss; persistent partial-write inconsistency.

Debug packet: sanitized input fingerprint, config versions, evidence IDs, tool outcomes, state transitions, verifier failures, timestamps, sufficient for replay without unnecessary secret exposure.
