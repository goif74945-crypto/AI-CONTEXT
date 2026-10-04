# Data & API Contracts
Operation: action/route, authn/authz, request/response/error schema, idempotency, pagination, ordering, filtering, timeout, rate limits, compatibility, invalid examples.
Error fields: code, message, request_id, details, retryable, retry_after, field_errors. Never branch on prose.
Field: type, nullability, meaning, units, range/domain, truth source, mutability, defaults, privacy, retention, migration.
Semantic changes can break compatibility even with unchanged JSON shape.
Pagination requires stable ordering/cursor semantics.
Idempotency keys bind caller + operation + normalized request; persist result; reject conflicting reuse; define retention.
