# Long-Horizon Handoff Protocol
Checkpoint fields: CHAT_ID/TASK_ID, objective, authoritative inputs, immutable constraints, exact allowed and forbidden mutation surfaces, completed work with evidence, in-progress work, unresolved decisions, failures, last verified state, next deterministic action, stop conditions.

Resume by reading checkpoint, verifying artifacts, detecting external changes, selectively invalidating stale evidence, continuing from the next deterministic action, and never reinterpreting completed scope without new authority.

Separate FACT, ASSUMPTION, UNKNOWN, DECISION, EVIDENCE.