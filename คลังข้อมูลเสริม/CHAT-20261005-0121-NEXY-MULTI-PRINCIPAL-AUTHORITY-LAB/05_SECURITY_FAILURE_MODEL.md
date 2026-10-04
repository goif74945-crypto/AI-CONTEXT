# MPAL Security and Failure Model

Status: `AI_PROPOSED / THREAT_MODEL / NOT_SECURITY_CERTIFICATION`

## Threats covered by the reference logic
- **Replay across requests:** receipt binds to canonical request SHA-256.
- **Replay across policy versions:** request/receipt bind to explicit policy version.
- **Duplicate counting:** identical duplicate principal receipt cannot count twice.
- **Contradictory evidence:** different receipts from one principal freeze.
- **Role/group substitution:** approver role must match configured group.
- **Cross-domain misuse:** approver must hold the request domain.
- **Maker-checker bypass:** requester approval can be excluded and quorum is rechecked.
- **Unknown action:** no rule means deny, not inference.
- **Stale/future receipt:** explicit evaluation tick controls validity.
- **Veto erased by ordering:** model checks order invariance.

## Threats not solved
This prototype does not prove identity authentication, credential security, signature verification, anti-collusion, policy-authority security, TSA/time security, durable audit, distributed consensus, tenant isolation, privacy/data residency, UI phishing resistance, revocation-race safety, DoS resilience, or formal correctness for arbitrary policies.

## Failure semantics
- invalid policy/request => FREEZE;
- known requester without permission => DENY;
- action without rule => DENY;
- receipt binding/structure contradiction => FREEZE;
- authorized veto/deny => DENY;
- valid incomplete quorum => PENDING;
- all authority gates satisfied => ALLOW.

FREEZE is reserved for integrity cases where selecting ALLOW/DENY would invent semantics.

## Adoption security gates
Before real integration require authenticated identities, signed/tamper-evident receipts, policy provenance/signing, immutable audit linkage, replay protection, authoritative revocation/tick semantics, abuse tests, and independent security review.
