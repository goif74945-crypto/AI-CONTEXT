# Security & Trust Boundaries
Authentication identifies. Authorization permits. Validation constrains. Audit proves.
Boundary inventory: caller/callee, credential, identity, authorization, accepted data, validation, secret exposure, logging restrictions, replay protection, abuse limits.
Controls: server authz, least privilege, deny default, secret isolation/rotation, size/rate limits, secure sessions, CSRF where relevant, contextual encoding, SSRF/path traversal/upload controls, dependency provenance, sensitive audit events.
AI threats: prompt injection, tool argument injection, authority confusion, exfiltration, malicious files, model output treated as authority, poisoned context, forged evidence.
Invariant: untrusted content may supply data, never authority.
