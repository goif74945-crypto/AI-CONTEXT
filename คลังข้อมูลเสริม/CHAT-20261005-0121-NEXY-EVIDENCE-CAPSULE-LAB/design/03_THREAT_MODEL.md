# Threat Model — Evidence Capsule Lab

## Assets
- integrity of original evidence lineage;
- confidentiality of undisclosed evidence fields;
- authenticity of capsule issuer;
- authenticity and purpose/audience binding of presentations;
- freshness and replay state;
- policy decision correctness.

## Adversaries considered
1. Consumer edits a disclosed value.
2. Consumer edits salt/proof/index.
3. Consumer swaps a presentation onto a different capsule.
4. Consumer changes audience/purpose/timestamp.
5. Consumer replays a once-consumed presentation.
6. Unauthorized role requests a restricted field.
7. Attacker presents an expired/stale bundle.
8. Attacker changes record metadata or Merkle root.
9. Attacker uses an unknown/wrong signing key.

## Reference mitigations
- domain-separated hashes;
- salted per-field commitments;
- Merkle inclusion proofs;
- authenticated header and presentation;
- content-derived IDs;
- audience binding;
- explicit validity/max-age checks;
- replay guard hook;
- fail-closed role policy;
- duplicate field/index rejection.

## Important limitation: HMAC
The reference uses HMAC-SHA256 only to keep the prototype dependency-free. A verifier that holds the shared HMAC key can forge issuer signatures. Therefore HMAC proves behavior of the protocol mechanics, not production issuer authenticity.

Production adoption requires an asymmetric signature scheme, key identity/rotation/revocation, protected signer boundary, and independent crypto review.

## Privacy limitations
Merkle commitments do not hide metadata such as field count, record/issuer identifiers, validity interval, presentation audience, role, purpose, number of disclosed fields, or timing. Salts reduce low-entropy commitment guessing but do not create zero-knowledge privacy.

## Out-of-scope threats
Endpoint compromise, traffic analysis, side channels, malicious runtime, compromised authoritative policy, coercion, hardware key theft, and cryptographic implementation bugs are not solved by this lab.

## Fail-closed rule
If integrity, authenticity, freshness, policy or replay status cannot be established at the required evidence class, the presentation is NOT VERIFIED and should not cross a NEXY release boundary.