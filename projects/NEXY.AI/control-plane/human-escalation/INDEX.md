# P4.15 Human Escalation

Records situations that require an external authorization decision.

Gate classes:
- destructive migration
- secret or credential handling
- production mutation
- authority/spec conflict
- irreversible data operation
- security-boundary expansion
- branch-history rewrite
- ambiguous destructive recovery
- cross-tenant effect

Escalation records never bypass the required decision.
