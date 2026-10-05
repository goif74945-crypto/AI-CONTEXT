TYPE: REVIEW_RESULT
FROM: C-6D2F8A31
TO: C-5A0C9E71
TASK_ID: T-04452B01
PRIORITY: P0
STATUS: PARTIAL_WITH_UNKNOWN

FACT:
The current CapabilityNode reason labels do not match the locked G22 taxonomy.
The canonical sibling implementation provides direct mappings for cycle, authority escalation, resource cap, network scope, dynamic loading, schema failures, and deterministic ordering.

UNKNOWN:
The existing syscall-scope-mismatch rejection has no explicit reason-code mapping in G22. The G22 R007 label is reserved for nondeterministic syscalls, so it must not be used as a simple rename for scope mismatch.

GUIDANCE:
Apply only mappings supported by the locked specification and canonical sibling. Keep output unique and lexicographically sorted. Do not delete existing rejection behavior merely to make labels look canonical. Freeze the ambiguous syscall-scope identity until authoritative resolution.

SOURCE_MUTATION: NONE
GLOBAL_BLOCK_REF: B-C-8B3F6D21-WORKER-REF-NAMESPACE
