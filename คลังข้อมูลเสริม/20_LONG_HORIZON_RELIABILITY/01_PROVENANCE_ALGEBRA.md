# Provenance Algebra
Status: PROPOSAL

## Problem
A citation is not enough. A conclusion may combine spec, repository state, runtime evidence and inference. Future systems need compositional rules that prevent a weak premise from laundering itself into a strong claim.

## Claim tuple
Represent each material claim C as:
C = <id, proposition, class, authority, scope, source_identity, dependencies, verifier, state>

class ∈ {SOURCE_FACT, REPO_FACT, RUNTIME_FACT, EXTERNAL_FACT, INFERENCE, ASSUMPTION, UNKNOWN, CONFLICT, NOT_VERIFIED}
state ∈ {VALID, STALE, SUPERSEDED, REVOKED, CONFLICTED, UNKNOWN}

## Composition laws
P1 Weakest-premise law: a derived claim cannot inherit a stronger evidence class than its weakest indispensable premise.
P2 Scope-intersection law: derived validity scope is the intersection of all indispensable premise scopes.
P3 Identity-binding law: repo/runtime claims bind to exact source identity where correctness depends on code state.
P4 No-authority-laundering: repeated summaries never increase authority.
P5 Conflict-preservation: unresolved contradictory premises produce CONFLICT, not averaged prose.
P6 Assumption-taint: an indispensable ASSUMPTION remains visible in every dependent conclusion.
P7 Revocation propagation: revoked or superseded indispensable premises invalidate dependent closure until recomputed.
P8 Negative-evidence distinction: absence of evidence is not evidence of absence unless the search contract establishes completeness.
P9 Verifier independence: self-attestation by the producing agent is metadata, not independent proof.
P10 Transform traceability: normalization/summarization must retain links to originals.

## Derivation record
{
  "claim_id": "...",
  "proposition": "...",
  "premises": ["..."],
  "transform": "rule/version",
  "result_class": "INFERENCE",
  "scope": {...},
  "source_identities": [...],
  "unresolved": [...],
  "created_by": "...",
  "reproducible": true
}

## Closure algorithm
1. Start at requested claim.
2. Traverse indispensable dependencies.
3. Reject missing nodes as UNKNOWN.
4. Detect cycles and require explicit fixed-point semantics; otherwise CONFLICT/UNKNOWN.
5. Validate source identities and supersession.
6. Compute scope intersection.
7. Compute weakest admissible class.
8. Surface assumptions/conflicts.
9. Return claim plus proof frontier, never prose alone.

## Useful queries
- Which claims depend on this SHA?
- Which conclusions become stale if spec X is superseded?
- Which PASS claims contain an assumption in their ancestry?
- Which claims have no independent verifier?
- Which derived statements have wider scope than their premises? (invalid)

## Adversarial cases
- ten AI summaries all repeat one unverified statement
- current code cited with old test evidence
- runtime PASS from different feature flag configuration
- authoritative spec quoted through an untrusted issue
- “all files checked” when search was paginated/truncated
Expected: no provenance strengthening; scope and incompleteness remain explicit.
