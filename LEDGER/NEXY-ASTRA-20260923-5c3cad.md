LEDGER_ID: NEXY-ASTRA-20260923-5c3cad
claims:
  - claim: Current repaired HEAD is 5c3cad685cc7500685349578485ba15bd286c3c9 at record time.
    proof: GitHub branch read after fast-forward repair commits.
    risk: branch may move later.
    status: VERIFIED_AT_TIMESTAMP
  - claim: Current-head CI is not executable evidence.
    proof: run 35886459382 primary jobs conclusion=failure with steps=null; downstream gates skipped.
    risk: environment-specific.
    status: VERIFIED
  - claim: Runtime suite was not executed in this repair round.
    proof: hosted steps absent; desktop offline; container clone DNS failure exit 128.
    status: VERIFIED
  - claim: Active implementation gaps remain.
    proof: no verified physical blob deletion adapter; archival lifecycle and durable live-config integration remain absent/incomplete.
    status: VERIFIED_SOURCE_AUDIT
confidence: high for listed current-head/source claims; runtime correctness unknown
freshness: 2026-09-23T16:06:49Z source timestamp
trace_id: NEXY-ASTRA-20260923-5c3cad
