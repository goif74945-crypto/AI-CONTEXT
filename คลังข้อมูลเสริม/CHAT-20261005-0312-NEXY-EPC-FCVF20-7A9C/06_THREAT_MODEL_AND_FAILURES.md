# Threat Model and Failure Semantics

## Threats in scope

The primary attacker is not necessarily a malicious person. It may be a buggy AI, a stale integration, a duplicated request, a permissive refactor, malformed evidence, an authority-confused adapter, or a future maintainer who weakens a rule because an inconvenient test is red.

FCVF specifically defends against repeated KEEP/CUT use, status laundering from WIP into CUT, partial evidence masquerading as a vote, duplicate claims without semantic proof, retrospective vote mutation, destructive CUT interpretation, binary-float decision paths, non-deterministic ordering, direct promotion, external Core mutation, Canon override, and stale/unpinned provenance.

## Fail-closed behavior

Invalid actions return a rejected `TransitionResult` with an explicit code and the prior immutable state. Arithmetic overflow/division-by-zero raises an explicit `Q64Error`. Canonicalization rejects binary floats. The engine never silently clips, wraps, defaults a missing proof to confidence, or converts an authority violation into DEFER.

## Regression adversary

The test suite has an intentional weak-model capability. Examples include `max_keep=2`, `allow_promotion=True`, `allow_core_mutation=True`, and `allow_canon_override=True`. These flags do not exist to make production permissive; they exist so the verifier can demonstrate that its independent invariant layer detects exactly the sort of rule regression it claims to detect.

## Residual risks

Bounded model checking is not unbounded formal proof. The event alphabet is a model, so an omitted future event type can introduce behavior not explored here. Python runtime correctness and SHA-256 collision resistance are trusted dependencies. This lab has no production, distributed, concurrency, database, hardware or deployment evidence. Integration with NEXY is proposed, not executed.

## Stop conditions

If an integration would require FCVF to write NEXY state, if authoritative sources conflict, if exact pins cannot be established, or if the implementation can pass only by weakening an immutable rule, the correct state is BLOCKED/NOT_VERIFIED rather than fabricated success.
