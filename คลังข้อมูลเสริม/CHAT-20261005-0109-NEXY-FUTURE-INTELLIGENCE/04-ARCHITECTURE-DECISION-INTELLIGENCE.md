# Architecture Decision Intelligence

Goal: make future decisions reversible, evidence-driven and auditable without assuming a specific NEXY.AI stack.

## Decision record
- decision_id
- problem
- context
- constraints
- immutable_requirements
- options
- evidence_for_each_option
- rejected_options + reason
- chosen_option
- reversibility: easy/moderate/hard/irreversible
- blast_radius
- migration_cost
- compatibility_surface
- observability_required
- rollback_plan
- validation_plan
- expiration/review_trigger

## Decision dimensions
Correctness; compatibility; failure isolation; data integrity; latency; throughput; cost; operability; debuggability; security; privacy; portability; vendor lock-in; migration complexity; cognitive load.

## Reversibility rule
Prefer reversible decisions when evidence is weak. Spend irreversible complexity only where evidence demonstrates durable value.

## Architecture fitness functions
Instead of prose-only principles, encode measurable constraints when possible:
- dependency direction constraints
- API compatibility tests
- schema compatibility checks
- latency budgets
- resource budgets
- forbidden import/dependency rules
- minimum observability fields
- deterministic error contracts

## Decision debt
A decision becomes debt when its original assumptions are invalid, evidence expires, scale changes, or a temporary workaround becomes structural.

## Review triggers
New authoritative requirement; repeated incident; performance threshold breach; security finding; dependency end-of-life; major scale shift; inability to test; rollback no longer viable.
