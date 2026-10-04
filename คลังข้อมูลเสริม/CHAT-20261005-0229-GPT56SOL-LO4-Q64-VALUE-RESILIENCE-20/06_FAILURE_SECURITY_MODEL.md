# Failure and Security Model

- **Malformed numeric input**: reject. No string-to-float convenience coercion.
- **Overflow**: reject with `Q64OverflowError`; never wrap or saturate silently.
- **Division by zero**: explicit exception. The one intentional `0/0` normalization in `ratio01` is defined as zero and unit tested.
- **Untrusted extra fields**: reject to prevent hidden semantic expansion.
- **Missing fields**: reject to prevent defaults from inventing evidence.
- **Low confidence**: release band returns `FREEZE`.
- **Replay drift**: canonical serialization and repeated byte-level execution are tested.
- **Authority escalation**: forbidden. Lo4 output is advisory until promotion.
- **Side effects**: none in evaluator package; pure computation only.
- **Secrets/network**: no credentials and no network dependency in the package.
