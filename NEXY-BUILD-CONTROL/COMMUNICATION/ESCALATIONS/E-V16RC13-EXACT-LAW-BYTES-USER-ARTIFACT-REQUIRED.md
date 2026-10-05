# E-V16RC13-EXACT-LAW-BYTES-USER-ARTIFACT-REQUIRED

ESCALATION_ID: E-V16RC13-EXACT-LAW-BYTES-USER-ARTIFACT-REQUIRED
TARGET_AUTHORITY_KEY: b11e0417b2731cdb032af51b723d555b1e06f275426ee85276f4254191d4cc93
REQUESTED_CONSTITUTION: NEXY::EQUAL-PEER-FENCED-ATOMIC-DYNAMIC-SCALE-ENGINEERING-CONSTITUTION-V16-RC1.3
CURRENT_PHASE: PHASE_1_STATIC_CONTROL_REPAIR
CONTROL_HEAD_OBSERVED: ad6ca1524d51ab6db2c172be9471b9a2532fcd33
STATUS: USER_ARTIFACT_REQUIRED
PRODUCT_MUTATION: NONE
TARGET_INTEGRATION: NONE

## Blocking finding

FINDING-V16RC13-EFFECTIVE-CONSTITUTION-BYTES-NOT-PINNED-001

The Constitution requires EFFECTIVE_CONSTITUTION_HASH to be SHA-256 of the exact canonical law bytes after:
- Unicode NFC
- LF line endings
- trailing whitespace removal per line
- normative ordering preserved
- UTF-8 encoding

No immutable exact V16-RC1.3 law-byte artifact is currently present in canonical control state.

## Why engineering cannot substitute a reconstruction

A model-retyped or manually reconstructed copy of the chat directive is not byte-identity evidence and must not be used to invent EFFECTIVE_CONSTITUTION_HASH.

The current chat/tool surface exposes the law semantically to participants but does not expose a tool-verifiable raw byte artifact for hashing and provenance binding.

## Required user artifact

Provide the exact effective V16-RC1.3 Constitution as an immutable byte artifact, preferably a UTF-8 .txt file containing the complete law text exactly once.

Alternative acceptable source:
- an immutable user-authorized file already stored in a repository/file surface whose exact bytes can be fetched and hashed.

Do not use:
- AI transcription,
- shortened/restated law,
- generated summary,
- reconstructed prompt text,
- inferred bytes.

## Validation after artifact is available

1. Hash the raw supplied artifact for provenance.
2. Apply clause [030] canonicalization deterministically.
3. Compute lowercase 64-hex SHA-256.
4. Independently recompute from the same raw artifact.
5. Persist the immutable raw/canonical artifact identities and EFFECTIVE_CONSTITUTION_HASH.
6. Bind later genesis/activation only to the independently verified hash.

## Stop condition

PHASE_3_ATOMIC_ACTIVATION remains forbidden until exact law identity is pinned and independently verified. Preactivation audit/control repair may continue.
