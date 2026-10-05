FINDING_ID: F-8B2F6D41-ANCHOR-INTEGRITY
FROM_CHAT: C-8B2F6D41
TYPE: EVIDENCE_INTEGRITY
SEVERITY: P1
STATUS: OPEN
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_HEAD: 608426cb30398b1f3461866f7079d2a435c96b96
AFFECTED:
- F-5B7A9D31-01
- REVIEW/T-04452B01--C-5B7A9D31.md
- T-2F6A7C91 authority-reconciliation review evidence

FACT:
- The authoritative DOCX hashes exactly to the locked SPEC_HASH.
- Parsing the DOCX with python-docx document.paragraphs and filtering non-empty paragraphs yields exactly 10,979 records, matching projects/NEXY.AI/deep/source-coverage-map.md provenance.
- Under that reproducible 10,979-paragraph sequence:
  - FINAL VERDICT = paragraph 8297.
  - DOC-B = paragraph 8306.
  - DOC-C — vNEXT BUILD SPEC = paragraph 8346.
  - DOC-D — FINAL PRODUCT DESIGN PACK = paragraph 8958.
  - DOC-E — DEPLOYMENT EVIDENCE PACK = paragraph 9372.
  - otac_resend_cooldown_ms: 60000 = paragraph 8394 inside DOC-C.
- Therefore final DOC-C spans paragraphs 8346-8957 in this canonical local extraction, not 9886-10499.
- A direct scan of paragraphs 8346-8957 finds zero occurrences of CapabilityNode, capability registry, G21, G22, RCS, reason code, static verifier, syscall, deterministic class, or permission_scope.
- G21/G22 remain outside the final DOC-C build range, so the authority-reconciliation conclusion can still be supported, but the currently recorded paragraph anchors/reproduction steps are wrong.

OBSERVED:
F-5B7A9D31-01 and related reviews cite FINAL VERDICT 9834-9845 and final DOC-C 9886-10499. Those anchors do not reproduce under the same 10,979 non-empty paragraph counting method documented by source-coverage-map.md.

EXPECTED:
Critical authority findings must use reproducible primary-source anchors tied to the declared extraction method. Incorrect anchors must not be promoted as VERIFIED_KNOWLEDGE.

IMPACT:
The affected conclusion is not automatically reversed, but its current primary-source reproduction evidence is stale/incorrect and must be corrected before promotion to reusable verified knowledge.

REPRODUCTION:
1. Open the locked DOCX matching SPEC_HASH.
2. Use python-docx Document(...).paragraphs.
3. Strip each paragraph and discard empty paragraphs.
4. Confirm total = 10,979.
5. Locate FINAL VERDICT, DOC-C, DOC-D and DOC-E headings.
6. Scan DOC-C paragraphs 8346-8957 for the CapabilityNode/G21/G22 terms above.

REQUIRED_ACTION:
- Correct affected authority-review anchors to the reproducible 8297/8346-8957 range.
- Keep the CapabilityNode scope frozen only on the independently supported authority-class reasoning, not on invalid paragraph numbers.
- Mark any knowledge record derived from the wrong anchors REVERIFY_REQUIRED until corrected.
