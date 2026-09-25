LEDGER_ID: NEXY-EXACT-HEAD-REPAIR-20260926
claim: source attachment matches canonical NEXY-IGNIS identity
proof: SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7; OOXML/DOCX detected; 10,979 non-empty paragraphs
status: VERIFIED

claim: exact implementation HEAD is db960dd163a9f50373b747ac922d735d1250cf3a
proof: GitHub branch/commit observation
status: VERIFIED

claim: baseline mapped locations remain present at exact current HEAD
proof: implementation refs 864/864 present; requirement implementation refs 3218/3218 present; test refs 1149/1149 present
status: VERIFIED_STATIC

claim: baseline semantic mapping cannot be promoted unchanged
proof: 107 unique mapped implementation paths changed blob content; 164 entities affected; 166 requirements touch changed implementation refs and 166 touch changed test refs
status: REVALIDATION_REQUIRED

claim: DOC-E E1-E12 are not current-head proof
proof: all 12 observed files report db52f9f1870b302f36653268513251d010f9726e; current HEAD match 0/12
status: VERIFIED_STALE

claim: current runtime suite is not verified
proof: exact-head GitHub Actions failed jobs were rerun and inspected primary jobs still reported zero executed steps; connected desktop executor is offline
status: NOT_VERIFIED_RUNTIME

verdict: PARTIAL_NON_DEPLOYABLE
trace_id: NEXY-EXACT-HEAD-REPAIR-20260926
