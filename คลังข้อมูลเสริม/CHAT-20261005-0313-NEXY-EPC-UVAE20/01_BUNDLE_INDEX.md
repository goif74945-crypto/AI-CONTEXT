# UVAE-20 Sealed Artifact Index

CHAT_ID: CHAT-20261005-0313-NEXY-EPC-UVAE20
AUTHORITY_CLASS: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING
ARTIFACT: NEXY EPC User Value & Agency Evidence Laboratory (UVAE-20)

## Sealed source bundle

The complete Design + Code + Tests + Evidence artifact is preserved as one deterministic tar.gz bundle encoded into six ordered Base64 text parts:

1. bundle/uvae20-source.tar.gz.b64.part-000
2. bundle/uvae20-source.tar.gz.b64.part-001
3. bundle/uvae20-source.tar.gz.b64.part-002
4. bundle/uvae20-source.tar.gz.b64.part-003
5. bundle/uvae20-source.tar.gz.b64.part-004
6. bundle/uvae20-source.tar.gz.b64.part-005

Exact Base64 length: 40,492 characters
Decoded tar.gz size: 30,369 bytes
Decoded tar.gz SHA-256: b93810095d8099450dbbac99cd8097a094f08cdecf10f9a203d493318f9526ad
Manifest SHA-256: b1a3d3e8a63286ed8d7ebe62eb737bd8f70d23836f7776584090a9c0dfba8bb1
Durable manifest entries: 59
Source + tests: 1,142 lines

Remote Git blob identity was read back after upload and matched the locally computed expected Git blob SHA for every part:
- part-000: a2f6b58ee99ab831ae9000243644ecdeef31a5bc / 10,000 chars
- part-001: a7d00499979bd20fe96c830efa867f12333a9132 / 10,000 chars
- part-002: 687d4b40b6b6375533106211937bf334f1859c93 / 10,000 chars
- part-003: 6b191ebaa76edf6f093893483b0b7ce8128b22ce / 5,000 chars
- part-004: eb3c7599e6f097121d6086951bba24503085a325 / 5,000 chars
- part-005: db9d0705c20df9e1f845d7a723c562b1bbbe672e / 492 chars

Because Git blob SHA covers exact content bytes plus length, equality with the independently computed local Git blob SHAs proves the persisted Base64 text is byte-identical to the locally verified bundle encoding.

## Reconstruction

From this directory:

```bash
cat bundle/uvae20-source.tar.gz.b64.part-* > uvae20-source.tar.gz.b64
base64 -d uvae20-source.tar.gz.b64 > uvae20-source.tar.gz
echo "b93810095d8099450dbbac99cd8097a094f08cdecf10f9a203d493318f9526ad  uvae20-source.tar.gz" | sha256sum -c -
tar -xzf uvae20-source.tar.gz
cd uvae20
sha256sum -c MANIFEST.sha256
./scripts/verify.sh
```

## Bundle contents

Human-readable design/evidence:
- README.md
- DESIGN.md
- INTEGRATION_CONTRACT.md
- THREAT_MODEL.md
- NOVELTY_MATRIX.md
- TEST_PLAN.md
- EVIDENCE.md
- PROVENANCE.md
- evidence/REPAIR_HISTORY.md
- MANIFEST.sha256

Implementation:
- CMakeLists.txt
- include/nexy_uvae/*.hpp
- src/q64.cpp
- src/model.cpp
- src/engine.cpp
- src/rule_support.hpp
- exactly 20 src/rules/*.cpp modules
- examples/inspect_candidate.cpp

Verification:
- tests/unit_main.cpp
- tests/property_main.cpp
- tests/integration_main.cpp
- tests/fixtures.hpp
- scripts/check_no_floats.py
- scripts/verify.sh
- captured GCC/Clang/ASan+UBSan evidence logs and hashes

## Twenty candidate systems

1. Explicit Intent Fidelity Gate
2. Choice Burden Meter
3. Cognitive Surface Budget
4. Explanation Compression Witness
5. Reversibility Visibility Index
6. Consent Scope Integrity
7. Interruptibility Contract
8. Resume Fidelity Gauge
9. Failure State Legibility
10. Error Recovery Actionability
11. Undo Horizon Witness
12. Preference Non-Inference Guard
13. Accessibility Determinism Audit
14. Locale Semantics Invariance
15. Low-End UX Resource Budget
16. Latency Transparency Contract
17. Notification Restraint Gate
18. Action Preview Fidelity
19. Evidence-to-Display Binding
20. User Data Agency Contract

## Protected scope statement

No write was performed against goif74945-crypto/NEXY.AI- or any repository name containing NEXY.AI. NEXY was inspected read-only only.
