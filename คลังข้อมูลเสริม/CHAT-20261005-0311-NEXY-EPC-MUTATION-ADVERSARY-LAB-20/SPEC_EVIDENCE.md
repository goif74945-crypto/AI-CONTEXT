# Direct Spec Evidence — NEXY-IGNIS

SOURCE_ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
DRIVE_OBJECT_OBSERVED_NAME: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.txt`
RAW_TYPE_DETECTED: `Microsoft Word 2007+ / OOXML DOCX`
RAW_SIZE_BYTES: `2146350`
RAW_SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
NONEMPTY_PARAGRAPHS: `10979`

The raw Drive object was downloaded and parsed directly as DOCX before the KEEP decision. The misleading .txt filename is provenance metadata only; the bytes are OOXML and the SHA-256 matches the canonical NEXY source identity already pinned by project context.

## Directly inspected authority evidence

Paragraph 2654: Canon is the single source of truth; unclear cases halt; contradictions freeze rather than being silently resolved.

Paragraph 2657: Core alone may decide, validate, verify, lock/freeze/kill, and commit to Vault.

Paragraphs 2658-2660: AI roles are limited to decomposition/debate/simulation/verification, and the multi-AI pipeline must halt on stage failure.

Paragraph 2662: Human Layer is usability-only; state mutation, decision override, and verification bypass are forbidden.

## Directly inspected numeric evidence

Paragraphs 6771-6775:
- signed 128-bit fixed-point;
- format Q64.64;
- authoritative math uses fixed128;
- no mixed precision.

## Directly inspected verification / dependency evidence

Paragraphs 8487-8494 require validation at UI/API/CORE/queue/worker/SWARM/JUDGE/LAW/VAULT boundaries.

Paragraphs 8517-8522 assign CORE orchestration, LAW rule enforcement, SWARM worker execution, and JUDGE evaluation.

Paragraphs 8546-8551 include forbidden dependency edges such as SWARM → VAULT and JUDGE → CORE.

Paragraphs 8626-8633 assign event ownership:
- execute = CORE;
- agents_done = SWARM;
- verified / accepted / rejected = JUDGE.

Paragraphs 9858-9863 restate the authority lock and explicitly forbid HUMAN LAYER from changing Core state.

## Relation to this Lo4 proposal

The mutation lab does not reinterpret these rules as new Canon. It uses them as known-invalid mutation targets so tests can demonstrate whether a verifier notices authority bypass, JUDGE omission, unauthorized state transition, non-Q64 authoritative numeric behavior, and verification bypass.

No claim of NEXY runtime integration is made from reading this specification.
