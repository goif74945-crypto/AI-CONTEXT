# BQPK Architecture

## Boundary
`untrusted claim envelope -> structural validation -> evidence normalization -> freshness classification -> proof bounds -> quantifier calculus -> fail-closed verdict`

## Modules
- `bqpk/core.py`: pure deterministic evaluator.
- `bqpk/cli.py`: filesystem/stdin boundary only; core remains I/O-free.
- `bqpk/__init__.py`: stable public API.
- `tests/test_core.py`: unit proof calculus and malformed-input tests.
- `tests/test_cli.py`: JSON boundary integration.
- `examples/*.json`: reproducible sample claims.

## Input contract
Required top-level fields:
- `claim_id: string`
- `predicate: string`
- `quantifier: ALL | NONE | EXACTLY | AT_LEAST | AT_MOST`
- `target_revision: string`
- `domain.population: string[]`
- `domain.enumeration.complete: boolean`
- `domain.enumeration.method: string`
- `domain.enumeration.evidence_ref: string`
- `evidence: EvidenceRecord[]`

Threshold is required for EXACTLY / AT_LEAST / AT_MOST.

Evidence record:
- `member_id`
- `outcome: MATCH | NO_MATCH | UNKNOWN | NOT_VERIFIED`
- `evidence_ref`
- `target_revision`

## Proof bounds
For observed evidence:
- `lower = count(MATCH)`
- unresolved = missing + stale + UNKNOWN + NOT_VERIFIED
- if domain enumeration is complete: `upper = lower + unresolved`
- if domain enumeration is incomplete: `upper = UNBOUNDED`

Known NO_MATCH values never increase upper.

## Quantifier rules
- ALL: PASS only when every bounded member is MATCH. Any NO_MATCH refutes.
- NONE: PASS only when bounded upper is 0. Any MATCH refutes.
- EXACTLY k: PASS only when lower == upper == k; FAIL if lower > k or finite upper < k.
- AT_LEAST k: PASS when lower >= k; FAIL only when finite upper < k.
- AT_MOST k: PASS when finite upper <= k; FAIL when lower > k.

Everything else is NOT_VERIFIED.

## Result contract
- `status: PASS | FAIL | NOT_VERIFIED`
- `action: RELEASE | FREEZE`
- `decision: PROVEN | REFUTED | INVALID | INSUFFICIENT_EVIDENCE`
- stable `reason_codes`
- proof metrics and affected member lists
- canonical SHA-256 input fingerprint when serializable

Only `status=PASS` can produce `action=RELEASE`.

## Security / failure semantics
- malformed structures fail closed;
- duplicate population/evidence IDs are invalid;
- evidence for members outside the declared domain is invalid;
- blank provenance is invalid;
- revision mismatch becomes stale/unresolved rather than silently accepted;
- population is capped to protect the reference implementation from accidental resource abuse;
- no dynamic code evaluation;
- no implicit filesystem/network access from the core.
