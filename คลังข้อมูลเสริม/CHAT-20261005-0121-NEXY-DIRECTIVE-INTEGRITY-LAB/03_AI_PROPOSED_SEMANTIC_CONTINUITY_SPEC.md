# AI-Proposed Semantic Continuity Specification

Status: **EXPERIMENTAL PROPOSAL — NOT NEXY CANON**

## 1. Objective
Preserve authorized directive meaning across transformations while allowing representation-specific normalization.

## 2. Semantic snapshot
Each boundary may emit a compact `DirectiveSnapshot` containing only fields that need continuity guarantees:
- stage;
- material action;
- target identity;
- constraints;
- in-scope resources;
- explicit out-of-scope exclusions;
- declared side effects;
- authority references;
- ambiguity state and clarification references;
- mutation class;
- impact class and risk-reassessment references;
- optional parent digest.

Set-like fields are canonicalized by trim, de-duplication, and lexical ordering. The snapshot is serialized as sorted compact JSON and SHA-256 hashed.

## 3. Transition invariant
Let `P` be the accepted parent snapshot and `C` a downstream snapshot. The default transition is legal only if all of the following hold or the affected path has an explicit evidence-backed authorization grant:

`action(C) = action(P)`  
`target(C) = target(P)`  
`constraints(P) ⊆ constraints(C)`  
`scope_in(C) ⊆ scope_in(P)`  
`scope_out(P) ⊆ scope_out(C)`  
`side_effects(C) ⊆ side_effects(P)`  
`authority_refs(P) ⊆ authority_refs(C)`  
`mutation_rank(C) <= mutation_rank(P)`

Impact may become lower only with one or more risk-reassessment references. OPEN ambiguity may become RESOLVED only with one or more clarification references.

If `C.parent_digest` is present, it must equal `SHA256(canonical(P))`.

## 4. Explicit re-authorization
Some legitimate workflows intentionally broaden scope or change a target. The verifier therefore does not hard-code “never change.” It requires an `AuthorizedDelta` bound to the exact semantic path and carrying:
- `path`;
- `evidence_ref`;
- `reason`.

The reference verifier rejects duplicate grants for the same path to avoid conflicting shadow authority.

A production design should further bind grants cryptographically to actor, target digest, expiry, and authority policy. That extension is intentionally not fabricated here.

## 5. Failure semantics
Any ungranted violation produces `FREEZE`, not a best-effort rewrite. Violations are machine-readable and include code, JSON-like path, parent value, child value, and concise operator message.

## 6. Determinism
The reference implementation avoids time, randomness, network, environment-dependent policy, and model inference. Equivalent set-like content yields the same digest regardless of insertion order.

## 7. Separation from CIRL/CLE
CIRL answers “what explicit intent can be resolved from normalized input?”  
CLE answers “what enforceable law follows from explicit resolved context?”  
Semantic continuity answers “did a downstream representation materially change what was already authorized?”

It must not infer missing intent, reinterpret prose, or promote AI-generated meaning to user authority.

## 8. Separation from execution transaction model
The existing transaction model tracks authorization, pre-state, side effects, idempotency, rollback/compensation, and verification of an actual action. Semantic continuity is earlier/narrower: it verifies that the transaction contract did not acquire unauthorized semantics while being derived.

## 9. Threat model
Primary threats include accidental mapper drift, lossy schema migration, agent/tool prompt overreach, stale transformation code, unsafe defaults, scope-exclusion loss, target aliasing, risk-class downgrade, and ambiguity laundering.

## 10. Evidence boundary
The 22-test reference suite establishes behavior of this standalone Python model only. It does not establish production compatibility, NEXY integration, runtime security, latency, or deployment readiness.
