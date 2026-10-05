REQ_ID: REQ-AUTH-0001
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_PAGE: UNKNOWN
SPEC_LINES: 9844-9854
SPEC_TEXT: FINAL VERDICT maps DOC-A..DOC-E and states Build obligation comes from DOC-C only; Deploy approval comes from DOC-E only.
AUTHORITY_CLASS: FINAL_VERDICT_AUTHORITY
EXPECTED_BEHAVIOR: Engineering build verdicts trace to active DOC-C clauses, constrained by DOC-B law; deployment approval traces to DOC-E evidence.
FORBIDDEN_BEHAVIOR: Treating vision/product/deployment text as equal build authority or letting implementation/tests override DOC-C.
AFFECTED_SYSTEMS: control-plane,spec-analysis,implementation,testing,integration,finalization
DEPENDENCIES: none
IMPLEMENTATION_PATHS: NEXY-BUILD-CONTROL/AUTHORITY/AUTHORITY_MAP.md
TEST_PATHS: authority-trace review against primary source
STATUS: VERIFIED
LAST_VERIFIED_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
