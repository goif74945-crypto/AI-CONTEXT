FINDING_ID: F-6A8F2F6A
FROM_CHAT: C-6A8F4D23
TO_CHAT: C-4E8A2C71
TASK_ID: T-2F6A7C91
HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
SEVERITY: P0
OBSERVATION: Current CapabilityNode authority marker uses /(?:\bkernel\b|\bauthority\b|\boverride\b)/i. Because underscore is a JavaScript word character, authority-like permission tokens containing an underscore immediately after those terms bypass R007. This is narrower than canonical sibling ncf-governance, which uses /kernel|authority|override/i.
EXPECTED: No upward/Kernel/authority/override permission escalation token should bypass static authority validation merely by extending the marker term with an underscore suffix.
ACTUAL: Executed regex proof at current source pattern: KERNEL_ADMIN:write => false, authority_proxy:read => false, override_token:use => false; canonical sibling marker returns true for all three. Since these prefixes are not in SCOPE_RANK and are not syscall: permissions, the current permission loop has no other R007 path for them.
REPRODUCTION:
1. At HEAD 5034debd, inspect packages/phase-f/universe/capability-node.ts AUTHORITY_ESCALATION_MARKER.
2. Evaluate current regex against KERNEL_ADMIN:write, authority_proxy:read, override_token:use.
3. Observe false for each.
4. Compare packages/phase-f/game/ncf-governance.ts marker /kernel|authority|override/i; observe true for each.
EVIDENCE: Exact current source at 5034debd; executable JavaScript regex comparison performed by C-6A8F4D23; canonical sibling ncf-governance source search.
SUGGESTED_DIRECTION: Align the marker semantics with the canonical sibling or otherwise reject authority-marker substrings before rank handling; add focused negative tests for underscore-suffixed variants. Do not broaden unrelated permission syntax policy.
