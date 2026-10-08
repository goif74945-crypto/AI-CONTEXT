# NEXY Codex Next Command Audit 004
R01 Re-query product HEAD before using 8b406a63.
R02 Re-query AI-CONTEXT HEAD before writeback.
R03 Unlock SPEC_SOURCE_ACCESS_BLOCKED using exact uploaded DOCX SHA, not Drive text copy.
R04 Preserve source locator provenance for every spec-derived reclassification.
R05 Apply P9844 build-authority rule: DOC-C only for build obligations.
R06 Apply P9845 deploy-authority rule: DOC-E only for deploy approval.
R07 AUTH-03: preserve early 10–15m prose conflict; do not let it override DOC-C 300000ms.
R08 SCOPE-01: use Section 17 exact include/exclude/deferred semantics.
R09 Do not promote release rows from local tests alone.
R10 Distinguish broader TSA architecture from final DOC-C vNEXT obligation.
R11 Source search currently finds injectTsaBatchTime production definition but callers only in tests; require fresh proof before mutation.
R12 Do not inject Date.now/new Date/system clock to make browser green.
R13 Do not create fake TSA signatures or bypass 2-of-3 verification.
R14 If vNEXT queue hard-depends on TSA without DOC-C authority, treat that dependency itself as a candidate implementation/scope defect.
R15 Trace enqueue/stale TTL semantics before changing queue time behavior.
R16 Browser 2 failures are symptoms; fix the first authoritative root cause, not UI assertions.
R17 bwrap source currently binds /usr,/lib,/lib64,/etc/ssl while command may live under /opt; confirm on current runner before patch.
R18 Sandbox fix may expose only a minimal trusted read-only runtime root; never bind arbitrary guest-selected host paths.
R19 Preserve anti-escalation rule: sandbox app cannot mount host FS itself or gain privileged container rights.
R20 Do not disable bwrap or downgrade isolation just to pass tests.
R21 Experimental 10 failures must remain failing until root cause is fixed; no skip/only.
R22 CI zero-step failures remain INFRA_BLOCKED/UNKNOWN cause, not code failure.
R23 AUTH-11/EVID-01..03 historical mismatches remain historical; do not rewrite old evidence.
R24 Reclassify matrix only from current-head evidence and exact authority.
R25 Review remaining 62 CURRENT_NOT_VERIFIED in bounded slices; no mass promotion from passing suite.
R26 Before every write, detect concurrent HEAD drift and recompute.
R27 Final project claim requires one frozen HEAD with full required rerun and DOC-E evidence.
R28 Same run must execute at least one safe READY action; no plan-only stop.
FINAL: CLOSED_FOR_THIS_ROUND