# Long-Horizon Execution State
Conversation history should not be canonical execution state.
Checkpoint object: objective_id, immutable_requirements, acceptance_criteria, verified_completed_items, unresolved_items, blockers, active_locks, evidence_refs, mutation_ledger, next_safe_action, state_version.
Checkpoint after consequential mutations, phase boundaries, major evidence updates, and before context compaction.
Resume rule: validate checkpoint freshness and external state before continuing. Never blindly replay old next_action after time has passed.
