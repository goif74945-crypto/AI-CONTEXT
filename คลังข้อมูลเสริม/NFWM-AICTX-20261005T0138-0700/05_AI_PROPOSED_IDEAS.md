# AI-Proposed Follow-on Ideas

Every item here is **conceptual only unless explicitly marked implemented**.

## A. Exact-violation fingerprint targeting

Current minimization targets a violation class code. A future version could bind the predicate to a stable fingerprint of rule + semantic entities, preventing a different same-code violation from becoming the minimized result.

Potential value: stronger incident lineage.

## B. Causal-slice minimization

Add declared parent-event IDs and causal edges, then minimize while preserving causal closure. This would prevent witnesses that are syntactically minimal but omit required causal ancestors.

Potential value: more faithful distributed-system reproduction.

## C. Privacy-aware witness projection

Define a policy that proves which fields are necessary for the violation predicate, then removes unrelated metadata before witness export.

Potential value: smaller privacy/security surface. This requires dedicated policy and abuse testing before adoption.

## D. Regression-fixture compiler

Convert a verified witness into a deterministic test fixture with source commit/profile/witness hashes embedded.

Potential value: turn one incident into a permanent regression guard without manually rewriting logs.

## E. Streaming pre-index

For very large traces, compute compact indices for rule-relevant event kinds before ddmin so each predicate evaluation avoids scanning unrelated payload-heavy events.

Potential value: large performance improvement while retaining deterministic semantics.

## F. Cross-build witness comparison

Given witnesses from two builds, compare invariant code, semantic event roles, and canonical identities without assuming equal sequence numbers.

Potential value: detect whether an incident is truly the same failure family across versions.

## Promotion rule

None of these ideas should enter NEXY.AI merely because this document exists. Promotion requires an authorized task, current target-state inspection, implementation, and matching verification evidence.
