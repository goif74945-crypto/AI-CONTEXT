# Architecture & Protocol — Evidence Capsule Lab

## Problem
NEXY separates source truth, implementation truth, runtime truth and deployment evidence. It also states that redaction may operate on derived/copied views without rewriting original audit lineage. The missing experimental question is how a derived view can reveal only authorized evidence while still proving that the revealed fields belong to an immutable evidence record.

## Proposed architecture
`SOURCE RECORD → CANONICALIZE → SALTED FIELD COMMITMENTS → MERKLE ROOT → SIGNED CAPSULE HEADER → POLICY FILTER → SELECTIVE PRESENTATION → VERIFIER`

### 1. Canonical record
The reference profile accepts JSON-like null/bool/int/string/list/object values, rejects floating point and non-string object keys, emits UTF-8 JSON with sorted keys and compact separators, and treats this profile as protocol-specific rather than universal canonical JSON.

### 2. Field commitments
Each top-level field is committed as:
`SHA256("NEXY-LEAF\0" || canonical(field_name) || 0x00 || canonical(value) || 0x00 || salt)`

A random salt prevents trivial dictionary attacks against low-entropy hidden values. Production salt lifecycle remains an adoption question.

### 3. Merkle commitment
Field leaves are ordered by UTF-8 field-name bytes. Internal nodes use domain-separated SHA-256. An odd node is duplicated. The capsule header publishes only the Merkle root and metadata.

### 4. Capsule header
The lab header binds protocol, reference signature algorithm, record identity, issuer, key id, issued/expires timestamps, nonce, field count and Merkle root. It is authenticated and assigned a content-derived capsule id.

### 5. Disclosure policy
The lab classifies fields as PUBLIC, INTERNAL, SENSITIVE or SECRET. The included role map is deliberately AI-proposed and non-canonical:
- PUBLIC_USER: PUBLIC
- OPERATOR: PUBLIC + INTERNAL
- AUDITOR: PUBLIC + INTERNAL + SENSITIVE
- OWNER/SYSTEM: all four

Production NEXY must derive policy from authoritative RBAC/policy state, not hard-code this experiment.

### 6. Selective presentation
A presentation includes only requested authorized values, their salts, Merkle proofs, role, purpose, audience, timestamp and nonce. It is authenticated separately from the capsule.

### 7. Verification
The verifier checks protocol, key lookup, header authentication, capsule id, presentation authentication/id, audience, validity interval, maximum age, replay id, duplicate disclosures, field indices, Merkle proofs and required-field presence.

## Failure semantics
Malformed, unauthorized, stale, replayed, or integrity-invalid bundles fail closed. There is no “best effort” partial success.

## Deliberate non-goals
No zero-knowledge proof, anonymous credential, network privacy, encryption-at-rest, production key management, cross-language canonicalization guarantee, or claim that this design is deployed in NEXY.