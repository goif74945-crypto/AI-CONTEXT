# Runtime Contracts
State machine: RECEIVED -> SCOPED -> EVIDENCE -> PLANNED -> EXECUTING -> VERIFYING -> COMPLETE|FIXING|BLOCKED.
Invariants: preserve requirements; never promote assumption to fact; bind consequential claims to evidence; distinguish successful call from successful objective; writes require target/precondition/postcondition; retries require duplicate-safety.
Tool result classes: SUCCESS_VERIFIED, SUCCESS_UNVERIFIED, RETRYABLE_FAILURE, NONRETRYABLE_FAILURE, CONFLICT, BLOCKED.
COMPLETE is illegal while a critical acceptance criterion is UNKNOWN or NOT VERIFIED.
Design value: makes autonomous behavior inspectable and testable without depending on conversational prose.
