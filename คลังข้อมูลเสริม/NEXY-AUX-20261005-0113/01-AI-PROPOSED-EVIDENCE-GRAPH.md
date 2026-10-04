# AI-PROPOSED CONCEPT — NEXY Evidence Graph & Proof Lineage Fabric
Status: PROPOSAL / NOT CURRENT BUILD REQUIREMENT / NOT IMPLEMENTATION PROOF

## Basis
SOURCE_FACT: NEXY emphasizes verified output or freeze, explicit authority, provenance, deterministic control, and separation of design/implementation/runtime/deployment evidence.
INFERENCE: At scale, flat test-result lists are insufficient for safe proof lineage.
AI_PROPOSED_CONCEPT: model proof as a typed graph evaluated deterministically.

## ClaimNode
- claim_id, normalized_claim, claim_type
- subject_identity + immutable revision
- required_evidence_classes (E0..E7)
- authority_source, scope, criticality
- current_status

## EvidenceNode
- evidence_id
- claim_id
- subject_identity/revision
- evidence_class
- producer_identity + verifier_identity
- environment_identity
- command_or_method
- result: PASS|FAIL|PARTIAL|BLOCKED|NOT_VERIFIED|UNKNOWN|CONFLICT
- artifact_refs + source_hashes
- freshness_policy + invalidation_keys
- limitations

## Edges
SUPPORTS, CONTRADICTS, DERIVED_FROM, INVALIDATED_BY, SUPERSEDES, DEPENDS_ON, APPLIES_TO, PRODUCED_BY.

## Deterministic PASS rule
PASS only when target/revision/environment match, required evidence classes exist, mandatory evidence passes, no unresolved equal/higher-authority contradiction exists, invalidation keys remain stable, freshness holds, and critical dependencies pass. Otherwise preserve the strongest truthful non-PASS state.

## Selective invalidation
Proposed keys:
source_tree_hash, dependency_graph_hash, schema_hash, policy_hash, runtime_image_digest, environment_fingerprint, toolchain_version, test_fixture_hash.
A change invalidates only proofs whose dependency closure intersects the changed key.

## Contradiction handling
Preserve both records → compare target/revision/environment → reject stale/non-applicable proof → if both apply set CONFLICT → obtain adjudication/new evidence. Never average evidence.

## Proof bundle
manifest + exact subject revision + claim set + evidence subgraph + hashes + verifier versions + environment fingerprint + unresolved limitations + seal/signature metadata when appropriate.

## Threats
evidence replay; artifact substitution; verifier impersonation; incomplete bundle presented as complete; environment mismatch; malicious fixtures; hidden nondeterminism; TOCTOU drift; low-authority evidence laundering.

## Potential integration (proposal only)
LAW defines proof policy; JUDGE resolves claim status; VAULT stores proof lineage; SWARM may produce candidate evidence but cannot self-authorize PASS; RUN blocks unsafe execution; VIEW renders proof summaries.

## Verification if promoted
E1 schema/static checks; E2 deterministic resolver tests; E3 ingestion/invalidation integration; E4 PASS→change→NOT_VERIFIED→re-proof flow; E5 crash/replay/concurrency; E6 exact deployment bundle binding.

## Edge cases
untrusted clock; verifier crash between artifact and ledger commit; divergent valid environments; opaque SaaS version; semantic claim rename; semantic change under stable ID; partial evidence mistaken for complete.

## Promotion gate
Explicit canonical mapping, DOC-B/C conflict check, ownership, retention policy, executable acceptance tests, security review.
