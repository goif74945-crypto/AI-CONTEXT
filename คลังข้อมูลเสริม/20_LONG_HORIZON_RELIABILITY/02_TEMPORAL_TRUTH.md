# Temporal Truth and Supersession
Status: PROPOSAL

## Thesis
“True” without “true for which era?” is a common source of AI-context corruption. Time itself is not authority, but version/supersession boundaries are.

## Temporal coordinates
Each durable fact SHOULD record:
- observed_at: metadata only
- valid_for_ref / commit / release / schema version
- valid_from_identity
- valid_until_identity when known
- supersedes / superseded_by
- revalidation_trigger
- historical_only boolean

## Truth categories
CURRENT: proven for current governing identity.
HISTORICAL: valid for an older identity; useful for archaeology only.
PERSISTENT_INVARIANT: explicitly established across a defined identity range.
FUTURE_INTENT: planned/speculative, not implementation truth.
STALE_UNKNOWN: once valid, current applicability unproven.
ANACHRONISTIC_CONFLICT: two claims from different eras incorrectly compared as simultaneous.

## Rules
T1 Newer timestamp does not automatically outrank stronger authority.
T2 A later implementation does not silently rewrite historical facts.
T3 “Still true” requires either unchanged dependency closure or fresh verification.
T4 Migration documents must state both source-era and target-era semantics.
T5 Deprecated registries remain searchable but must be excluded from current denominators.
T6 Counts are especially temporal: every count needs dataset identity and completeness contract.
T7 Future intent cannot satisfy current implementation claims.
T8 A renamed concept needs identity mapping, not string similarity.

## Revalidation triggers
- governing requirement changed
- source tree changed in dependency cone
- toolchain/runtime changed materially
- feature flag/config changed
- evidence schema/verifier changed
- data corpus changed
- authority rank changed

## Anti-anachronism test
Given A(valid at commit X) and B(valid at commit Y):
1. determine whether X and Y share semantic era;
2. map supersession;
3. compare only if the question explicitly spans eras;
4. otherwise select current authorized era or return CONFLICT/UNKNOWN.

## Long-term payoff
This enables safe historical debugging, migration analysis, regression attribution and prevents old “facts” from re-entering current context merely because embeddings consider them relevant.
