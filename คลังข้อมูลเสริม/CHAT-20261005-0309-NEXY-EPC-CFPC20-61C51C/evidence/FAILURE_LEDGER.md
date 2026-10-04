# CFPC-20 Failure / Repair Ledger

## F-01 Strict compiler failure
Observed:
- sign-conversion warning in JSON escaping under `-Wsign-conversion`;
- unused test helper under `-Werror`.

Correction:
- explicit char-to-unsigned-char conversion;
- removed unused helper.

Re-verification:
- full Release configure/build/test rerun.
- PASS.

## F-02 Sanitizer link-contract failure
Observed:
- library objects were ASan/UBSan-instrumented;
- `cfpc_example` lacked sanitizer link flags;
- linker rejected unresolved sanitizer runtime symbols.

Correction:
- sanitizer compile/link flags added to every executable linking the instrumented library.

Re-verification:
- clean sanitizer rebuild;
- tests 60/60 PASS;
- example PASS.

## F-03 Certificate under-binding discovered during audit
Observed:
- first certificate design bound evaluated results but did not bind the full resource policy, assumptions, verification obligation sets and degradation contract.
- two policies could therefore theoretically share a result certificate.

Correction:
- certificate canonical record now binds exact raw Q64 budgets, canonical symbolic expressions, sorted assumptions, required/provided verification sets and degradation flags.
- resource claims and monomial terms canonicalized independently of insertion order.

Re-verification:
- identical logical policy with reversed resource/term order => identical certificate.
- changed budget => changed certificate.
- changed assumption => changed certificate.
- changed verification set => changed certificate.
- full GCC/Clang/ASan suites rerun, 60/60 each.

## F-04 AI-CONTEXT publication race
Observed:
- GitHub Contents API returned 409 because concurrent chats advanced main between expected and actual HEAD.

Correction:
- no force push;
- no overwrite;
- additive unique-path retries against current main.

Re-verification:
- source/test read-back exact Git blob identity: 9/9 MATCH.

## F-05 Direct authoritative spec read unavailable
Observed:
- Google Drive located `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.txt`, size 2,146,350 bytes.
- default fetch failed UTF-8 decoding.
- raw fetch path also returned connector decode error despite raw flag.
- metadata/source context is consistent with the known OOXML/DOCX-container issue, but the direct authoritative bytes were not successfully decoded in this execution.

Consequence:
- KEEP vote NOT consumed.
- CUT vote NOT consumed.
- current vote status = DEFER / INSUFFICIENT_DIRECT_SPEC_READ.
- normalized AI-CONTEXT spec evidence may constrain the Lo4 build but does not satisfy the user's stricter pre-vote direct-read law.
