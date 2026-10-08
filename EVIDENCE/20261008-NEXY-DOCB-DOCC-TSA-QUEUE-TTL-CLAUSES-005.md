# NEXY DOC-B / DOC-C Time Authority and Queue TTL Source Extract

SOURCE: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
PARAGRAPH LOCATOR RULE: Pnnnn = one-based ordinal of python-docx Document.paragraphs, not physical page number.
STATUS: VERIFIED_SOURCE_EXTRACT; NO_CODE_FIX_AUTHORIZED_BY_THIS_EXTRACT_ALONE

## FINAL AUTHORITY

- P09837: `DOC-A = VISION CANON`
- P09838: `DOC-B = SYSTEM LAW`
- P09839: `DOC-C = BUILD SPEC`
- P09843: `No document may mix all five as equal build authority.`
- P09844: `Build obligation comes from DOC-C only.`
- P09845: `Deploy approval comes from DOC-E only.`

## FINAL DOC-B

- P09846: `1) DOC-B — SYSTEM LAW CANON`
- P09858: `CORE may decide / validate / verify / enforce / freeze / kill`
- P09875: `1.5 Freeze Law`
- P09877: `confidence below threshold`
- P09878: `evidence insufficient`
- P09879: `unresolved contradiction`
- P09880: `policy conflict`
- P09881: `undefined behavior`
- P09882: `=> FREEZE`
- P09883: `No patch`
- P09884: `No guess`
- P09885: `No mask`

## FINAL DOC-C

- P09886: `2) DOC-C — vNEXT BUILD SPEC`
- P09896: `queue + idempotency`
- P09910: `2.3 Canonical Defaults`
- P09912: `export const VNEXT_DEFAULTS = {`
- P09945: `  queue: {`
- P09946: `    stale_job_ttl_ms: 900000,`
- P09947: `    max_concurrent_pipeline_runs: 10,`
- P09948: `  },`
- P10153: `POST /api/directives`
- P10155: `Purpose:`
- P10156: `create directive + pipeline run`
- P10161: `Idempotency:`
- P10162: `required`
- P10163: `Retry:`
- P10164: `same key returns same accepted run`

## BROADER TIME

- P04001: `IV. TIME POLICY`
- P04003: `Dual Source Time: Primary = TSA Witness = Chain timestamp`
- P04005: `TSA_SET_SIZE = 3 VALID_SIGNATURES >= 2`
- P04007: `DEGRADED_TIME_MAX = 24h After 24h without 2-of-3 TSA → Freeze anchor mutation`
- P04009: `ΔT_max = fixed constant If |TSA_time - Chain_time| > ΔT_max → ANOMALY flag`
- P05151: `6️⃣ SYSTEM CLOCK ACCESS`
- P05152: `A) Core cannot read system clock`
- P05153: `Allowed:`
- P05154: `TSA-injected batch time only`
- P05155: `Forbidden:`
- P05156: `Date.now`
- P05157: `system_time`
- P05158: `monotonic_clock`

## EARLIER QUEUE LAW

- P09435: `13. ASYNC / QUEUE LAW`
- P09439: `13.1 Job States`
- P09441: `QUEUED`
- P09442: `RUNNING`
- P09443: `SUCCEEDED`
- P09444: `FAILED`
- P09445: `CANCELLED`
- P09446: `EXPIRED`
- P09448: `13.2 Rules`
- P09450: `idempotency_key prevents duplicate execution`
- P09451: `FREEZE cancels pending release jobs`
- P09452: `STOP cancels all jobs`
- P09453: `failed job is NOT auto retried unless explicitly configured and non-deterministic risk = none`
- P09454: `stale queued jobs expire after configured TTL`
- P09456: `13.3 Queue Payload Validation`
- P09458: `validate before enqueue`
- P09459: `validate before consume`

## DOC-E PROOF

- P10917: `9) DOC-E — DEPLOYMENT EVIDENCE PACK`
- P10983: `9.6 Queue Readiness Proof`
- P10984: `Plain text`
- P10985: `Must prove:`
- P10986: `- enqueue works`
- P10987: `- worker consumes`
- P10988: `- invalid payload freezes correctly`
- P10989: `- stale jobs expire`
- P10990: `- idempotency blocks duplicates`

## Full-range literal-search audit

Final DOC-B P09846-P09885 has no literal occurrences of TSA, clock, verified time, authoritative time, time source, stale_job_ttl_ms, queue, expiry, expire, or TTL.
Final DOC-C P09886-P10916 has no literal occurrences of TSA, clock, verified time, authoritative time, time source, or expiry. It does include `stale_job_ttl_ms` exactly at P09946.
This negative search is a scoped absence of these literal terms, NOT proof there is no indirect dependency across documents, code, or synonyms.

## Determination

- The final DOC-C fixes stale_job_ttl_ms=900000 (15 minutes) and queue max_concurrent_pipeline_runs=10; it does NOT explicitly say queue TTL calculation must receive a TSA-signed time or validate 2-of-3 TSA witnesses.
- The final short DOC-B SYSTEM LAW CANON section similarly contains no queue expiry time-source clause.
- Earlier broader design text explicitly prohibits Core system-clock reads and allows TSA-injected batch time, and separately states a 3-TSA/2-valid-signatures authority and queue stale-expiry; these are not an explicit end-to-end requirement that final DOC-C canonical queue expiry verifies TSA.
- The current product source may still rely on TSA by its own architecture; Codex must inspect source->dependency->normative authority before changing queue time behavior. Never swap in Date.now(), bypass verified time where actually required, fabricate signatures, or loosen queue expiry.
- If the chain of authority remains undecidable, freeze TSA-path mutation only and continue independent sandbox/audit work.

## Full literal match positions

```json
{
  "final_doc_b": {
    "tsa": [],
    "clock": [],
    "verified time": [],
    "authoritative time": [],
    "time source": [],
    "stale_job_ttl_ms": [],
    "queue": [],
    "expiry": [],
    "expire": [],
    "ttl": []
  },
  "final_doc_c": {
    "tsa": [],
    "clock": [],
    "verified time": [],
    "authoritative time": [],
    "time source": [],
    "stale_job_ttl_ms": [
      9946
    ],
    "queue": [
      9896,
      9945
    ],
    "expiry": [],
    "expire": [
      9976,
      10096,
      10102,
      10126
    ],
    "ttl": [
      9932,
      9936,
      9946,
      10863
    ]
  }
}
```