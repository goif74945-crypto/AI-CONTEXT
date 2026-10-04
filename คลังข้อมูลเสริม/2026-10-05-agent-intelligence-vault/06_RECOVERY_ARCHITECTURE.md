# Recovery Architecture
Recovery is a first-class capability, not a retry loop.
Failure dimensions: transient/permanent; local/systemic; before/after mutation; detectable/silent; deterministic/nondeterministic.
Recovery policy: classify -> preserve evidence -> isolate affected state -> choose smallest correction -> execute -> verify -> regression test -> resume.
Retry budgets should be operation-specific. A transient read can retry aggressively; a non-idempotent external write may require zero automatic retries.
Store failure fingerprints so repeated failures can bypass already-proven bad strategies.
