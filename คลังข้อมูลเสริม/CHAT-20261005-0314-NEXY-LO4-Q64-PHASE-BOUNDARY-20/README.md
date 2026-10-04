# NEXY Lo4 Q64 Phase-Boundary Assurance 20

CHAT_ID: `CHAT-20261005-0314-NEXY-LO4-Q64-PHASE-BOUNDARY-20`
AUTHORITY: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

This folder preserves a verified standalone reference package containing Design + Code + Tests + Evidence for 20 deterministic Q64.64 phase-boundary / regime-shift assurance mechanisms.

## Artifact layout
The exact tested package is preserved as four binary chunks:
- `bundle/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part00`
- `bundle/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part01`
- `bundle/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part02`
- `bundle/NEXY-Lo4-Q64-Phase-Boundary-Assurance-20.tar.gz.part03`

Reconstruct with `bundle/ASSEMBLE.sh`. Expected archive SHA-256:
`5b5511bd3139039fdb1c0b96717e4abfe5d22ce7bf24957556c535fd3ce5b6c1`.

The archive was extracted into a fresh workspace, its internal package SHA-256 manifest was verified, rebuilt with GCC 14.2, and CTest passed 1/1 from the reconstructed bundle.

## Verification summary
- GCC 14.2 warnings-as-errors: PASS
- Clang 17 warnings-as-errors: PASS
- Clang 17 ASan + UBSan: PASS
- deterministic replay: PASS
- Q64 raw mathematical oracle: >30,000 rational operand-pair checks PASS
- exact 20 mechanism IDs: PASS
- negative paths / invalid domains: PASS
- static forbidden-token scan: PASS
- fresh-extraction bundle build + CTest: PASS

## Protected boundary
No write was made to any repository whose name contains `NEXY.AI`. NEXY implementation was inspected read-only only for compatibility evidence.

## Vote state
KEEP consumed: 0/1
CUT consumed: 0/1
Current status: DEFER / INSUFFICIENT_EVIDENCE for formal vote because the original authoritative DOCX bytes were not directly opened in this tool session and exhaustive semantic uniqueness is not proven.
