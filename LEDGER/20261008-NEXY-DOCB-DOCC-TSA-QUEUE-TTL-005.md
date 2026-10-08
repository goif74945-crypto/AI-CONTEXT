# LEDGER — NEXY Final DOC-B/C Time & Queue TTL 005

TASK_ID: 20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-005
MODE: CROSS / AUDIT
STATUS: VERIFIED_WITH_LIMITS
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_SOURCE: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
EVIDENCE: EVIDENCE/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-CLAUSES-005.md

| ID | Source locator | Claim | Proof | Dependencies | Risk | Status |
|---|---|---|---|---|---|---|
| 001 | DOCX binary | Required SHA matches exactly | SHA-256 computed over uploaded bytes | original file | file may not be accessible in Codex runtime | VERIFIED |
| 002 | P09837-P09845 | DOC-B=SYSTEM LAW; DOC-C=BUILD SPEC; DOC-C controls build obligation | exact paragraph text | authority classification | broader architecture may still constrain CORE | VERIFIED_SOURCE |
| 003 | P09846-P09885 | Final short DOC-B contains no queue TTL / TSA time-source clause | exhaustive literal search of bounded DOC-B span | synonym/indirect dependency possible | negative finding bounded only | VERIFIED_BOUNDED_NEGATIVE |
| 004 | P09886-P10916 | Final DOC-C does not explicitly name TSA, clock or verified time as queue expiry authority | exhaustive literal search of bounded DOC-C span | indirect cross-ref or synonym possible | do not infer arbitrary clock is authorized | VERIFIED_BOUNDED_NEGATIVE |
| 005 | P09945-P09948 | Queue stale_job_ttl_ms=900000; max_concurrent_pipeline_runs=10 | exact paragraph text | source config binding | runtime semantics need tests | VERIFIED_SOURCE |
| 006 | P10153-P10164 | Directive submission creates run and requires idempotency | exact paragraph text | endpoint semantics | no explicit TSA assertion | VERIFIED_SOURCE |
| 007 | P04003-P04009 | Broader dual-source 3 TSA, two valid signatures, 24h degraded bound | exact paragraph text | applicability to vNEXT must be proved | do not assume final DOC-C requirement | VERIFIED_SOURCE |
| 008 | P05151-P05158 | Broader Core forbids system clock, permits TSA injected batch | exact paragraph text | Core boundary | cannot simply replace with Date.now | VERIFIED_SOURCE |
| 009 | P09435-P09459 | Earlier queue law requires stale jobs expire after configured TTL, validation before enqueue/consume | exact paragraph text | source queue implementation | no explicit TSA linkage here | VERIFIED_SOURCE |
| 010 | P10983-P10990 | DOC-E requires actual queue readiness proof incl stale expiry | exact paragraph text | execution | not currently release proof | VERIFIED_SOURCE |
| 011 | source-specific absence | Explicit DOC-C mandate for TSA verification of queue TTL is not established by final DOC-C | bounded search + exact clauses | complete source dependency review | cannot authorize automatic removal of TSA | VERIFIED_WITH_LIMITS |

VERDICT: No explicit final DOC-C queue TTL TSA-verification requirement is found; do not infer a safe implementation patch from this negative result alone.
ROLLBACK: AI-CONTEXT-only forward revert after HEAD requery.
