# NEXY Supply-Chain Sentinel — Design

Status: `AI-PROPOSED SUPPLEMENTAL DESIGN`, not an authoritative NEXY.AI requirement.

## Purpose
Provide a small deterministic sidecar that turns dependency evidence into a canonical inventory, seals it with SHA-256, compares a candidate inventory to an approved baseline, and returns exactly one machine-readable decision: `ALLOW` or `FREEZE`.

This complements NEXY principles: no silent guessing, explicit provenance, deterministic behavior, evidence before trust, and freeze on unsupported or ambiguous states.

## Non-goals
- It is not a package installer.
- It does not contact package registries or the internet.
- It does not claim a dependency is safe or vulnerability-free.
- It does not modify NEXY.AI.
- It does not replace SCA/SBOM/signature systems.

## Trust boundary
All manifests, lockfiles, snapshots, policy JSON and package metadata are untrusted input. The sentinel performs local parsing only and has no network, process-spawn, credential, package-install, or filesystem mutation beyond caller-requested output writing.

## Supported evidence inputs (v0.1)
1. npm `package-lock.json` lockfileVersion 2/3 package maps.
2. Python `requirements.txt` entries using exact `name==version` pins, optionally with `--hash=sha256:<hex>`.

Anything outside those grammars is represented as a violation and causes `FREEZE` under the strict/default policy.

## Core data flow
`LOCK INPUT -> PARSE -> NORMALIZE -> POLICY CHECK -> CANONICALIZE -> SEAL -> SNAPSHOT`

`BASELINE SNAPSHOT + CANDIDATE SNAPSHOT -> VERIFY SEALS -> DIFF -> POLICY -> ALLOW | FREEZE`

## Determinism law
- Package records are canonicalized and sorted.
- JSON hashing uses UTF-8, sorted keys, fixed separators, no wall-clock field.
- Reasons and drift events are sorted by stable tuple keys.
- No network, randomness or current time participates in decision logic.

## Package identity
Logical identity: `(ecosystem, normalized_name)`.
Artifact identity: `(ecosystem, normalized_name, version, source, integrity)`.

Multiple artifact identities for one logical identity are permitted in a snapshot because real dependency graphs may contain multiple versions.

## Snapshot integrity
Each snapshot includes:
- schema version;
- source kind and SHA-256;
- normalized package records;
- parse/policy violations;
- inventory SHA-256 over canonical package records;
- snapshot SHA-256 over all sealable fields except the snapshot hash itself.

Loading a snapshot re-computes both digests and fails closed on mismatch.

## Drift event classes
- `ADDITION`
- `REMOVAL`
- `VERSION_CHANGE`
- `SOURCE_CHANGE`
- `INTEGRITY_CHANGE`

The classifier prefers a semantic change event when a one-to-one logical package mapping exists; otherwise it uses deterministic ADDITION/REMOVAL events for multi-version graph changes.

## Policy model
Default policy is strict:
- require integrity evidence;
- allow only HTTPS npm registry sources from configured hosts;
- deny additions, removals, version changes, source changes and integrity changes;
- reject unsupported inputs;
- cap inventory size and raw input byte size before parsing;
- reject credential-bearing or query-bearing package source URLs and persist only sanitized source identity.

Policies are plain JSON and validated fail-closed. Unknown policy fields are rejected to prevent typo-driven weakening.

## Failure behavior
Any parser ambiguity, unsupported construct, invalid digest, malformed snapshot, policy violation, or unauthorized drift produces `FREEZE` with stable reason codes. The implementation never converts incomplete evidence into `ALLOW`.

## Integration contract
NEXY.AI may invoke this project later as a pre-execution or release-gate sidecar. Integration should pass immutable input bytes + policy and consume JSON output. This project does not grant itself authority to mutate NEXY state.

## Security notes
- Zero third-party runtime dependencies reduces bootstrap/supply-chain surface for the sentinel itself.
- No shell execution.
- No URL fetching.
- File reads are explicit caller paths.
- Snapshot digests are integrity checks, not cryptographic signatures or identity attestation.
