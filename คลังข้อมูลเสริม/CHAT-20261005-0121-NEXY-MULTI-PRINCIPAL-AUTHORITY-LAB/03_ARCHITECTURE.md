# MPAL Architecture

Status: `AI_PROPOSED / EXPERIMENTAL`

## Purpose
Turn multi-principal authorization into a deterministic state transition rather than a conversational judgment.

## Actors
- **Requester** — principal asking for the protected action.
- **Approver** — principal able to contribute to a configured approval group.
- **Veto principal** — role authorized to deny under the rule.
- **Policy authority** — external authoritative mechanism that creates/version-controls the policy. MPAL does not grant itself this authority.
- **Evaluator** — deterministic reference engine that validates and evaluates supplied facts.
- **NEXY Core/Law/Judge** — future integration authority if this proposal were ever adopted. Not implemented here.

## Data flow

```text
VERSIONED POLICY
      +
BOUND REQUEST  ---- canonical SHA-256 ----+
      +                                  |
APPROVAL / VETO RECEIPTS ----------------+
      |
      v
VALIDATE STRUCTURE + SATISFIABILITY
      |
      v
BIND RECEIPTS TO REQUEST + POLICY VERSION
      |
      v
FILTER NON-AUTHORITATIVE RECEIPTS
      |
      v
APPLY VETO / DENY POLICY
      |
      v
COUNT DISTINCT QUORUM MEMBERS
      |
      v
ALLOW | DENY | PENDING | FREEZE
```

## Determinism model
The reference evaluator deliberately avoids wall-clock reads, randomness, network I/O, database reads, environment-dependent policy lookup, and model inference.

Time validity is represented by an explicit integer `evaluation_tick` supplied by the caller. A future authoritative integration would need to define which trusted time/event authority supplies it.

## Canonical fingerprints
`policy_sha256` and `request_sha256` are computed from recursively canonicalized JSON:
- mapping keys sorted;
- lists of identified principal/rule/group objects sorted by stable identity;
- lists of strings sorted;
- compact UTF-8 JSON encoding;
- SHA-256 digest.

These hashes bind content in this prototype. They are **not digital signatures** and do not authenticate the creator.

## Fail-closed boundary
`FREEZE` is returned for authority-integrity failures such as malformed policy/request/approval, ambiguous selectors, unknown authority identities where interpretation would be unsafe, request/policy binding mismatches, contradictory receipts, impossible requester-specific quorum, and group/role/domain mismatch.

`DENY` is used where policy gives a legal negative answer. `PENDING` means the request remains legally possible but lacks enough current approval evidence.

## Complexity
For validated policy size `P`, groups `G`, and approvals `A`, the reference evaluator is approximately linear in the represented data sizes. It is not a general SAT/SMT solver.

## Integration boundary
A production design would separately require authenticated identity, signed receipts, append-only audit storage, policy lifecycle/rollback, revocation propagation, tenant isolation, authoritative time, and a UI that exposes counted/ignored/missing/veto authority without fabricating success.
