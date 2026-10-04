# Future Ideas — AI-Proposed Only

Status: CONCEPT BACKLOG / NOT REQUIREMENTS

## A. Proof-carrying transformation adapters
Each mapper could emit `{input_digest, output_digest, adapter_version, declared_delta, authority_proof}`. A generic verifier would reject undeclared material deltas. This would make transformation code itself auditable rather than trusting mapper reputation.

## B. Capability lattice instead of string scope
Replace string resources with typed capability tuples such as `(resource, verb, effect, boundary)`. Scope broadening then becomes a partial-order check rather than brittle string comparison.

## C. Semantic migration certificates
When snapshot schema evolves, migration code could produce a certificate proving which fields were preserved, renamed, split, or intentionally re-authorized. This attacks schema-evolution drift.

## D. Differential adapter testing
Run multiple independent transformation adapters over the same accepted snapshot and compare canonical semantic outputs. Divergence becomes an evaluation signal, not an automatic truth vote.

## E. Counterfactual authorization tests
For every permission grant, automatically mutate one protected dimension (target, effect, scope, impact) and prove the verifier freezes. This turns “least authority” into negative-path regression evidence.

## F. Authority freshness and revocation
Future grants should carry freshness/revocation semantics. A semantically valid grant may still be unusable after role/session/policy state changes.

## G. Privacy-minimized semantic receipts
Persist digests and typed deltas without raw directive text where possible, reducing audit-data exposure while retaining traceability.

## H. User-facing change preview
Before consequential re-authorization, show a compact diff: “Target unchanged; write permission added; one new side effect; impact remains HIGH.” This supports informed control without exposing internal model deliberation.

## I. Semantic blast-radius score
A derived, non-authoritative metric could summarize how many protected dimensions changed. It must never replace individual hard gates and would require calibration before product use.

## J. Cross-agent scope conservation eval
During multi-agent decomposition, union all child scopes/side effects and verify they do not exceed the parent envelope unless explicitly delegated. This could catch authority amplification by task splitting.
