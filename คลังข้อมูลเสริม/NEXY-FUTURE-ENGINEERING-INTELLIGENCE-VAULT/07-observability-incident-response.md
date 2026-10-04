# Observability & Incident Response
Telemetry answers: what failed, for whom/how badly, why.
Propagate request/trace/operation IDs across services, queues, workers, external calls.
Structured logs: timestamp, severity, service, environment, request_id, trace_id, operation_id, actor_class, event, result, error_code, latency_ms, dependency, release_version. Exclude secrets/needless PII.
Metrics: traffic, errors, latency distribution, saturation, queue depth/age, retries, dependency health, cache, stuck workflows, freshness.
Alert on user impact/imminent exhaustion; every alert needs owner, severity, runbook, dedupe, recovery signal.
Incident loop: DETECT -> TRIAGE -> CONTAIN -> DIAGNOSE -> RESTORE -> VERIFY -> LEARN.
After restore verify baseline errors, backlog drain, consistency, no stuck workflows, synthetic critical paths, security controls.
