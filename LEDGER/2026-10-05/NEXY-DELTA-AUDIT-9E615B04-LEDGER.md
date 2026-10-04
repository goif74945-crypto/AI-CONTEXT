LEDGER_ID: NEXY-DELTA-AUDIT-9E615B04
head: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
tree: a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c
base_head: 9c1472615d08af96188953fa17b855d8ac45ba31
spec_sha256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

entries:
- L001 VERIFIED: 12 commits ahead, 42 changed/added paths, no deletes.
- L002 VERIFIED: 42/42 delta paths read; 839 unchanged blobs reuse prior exact content read; current file accounting 881/881.
- L003 VERIFIED: canonical DOCX hash unchanged.
- L004 VERIFIED: logical tick and TSA elapsed-time accessor are now distinct.
- L005 VERIFIED_WITH_LIMITS: LO2/I/O/queue consumer semantics materially improved and fail closed without TSA.
- L006 BLOCKER: no production injectTsaBatchTime caller found.
- L007 VERIFIED: targeted Phase-F localeCompare usages replaced by canonical comparator.
- L008 PARTIAL: repository scanner has end-to-end tests and expanded roots, but Phase-F remains OBSERVE/advisory.
- L009 RISK: deterministic Observability incident arbitration still contains localeCompare and is not blocked by scanner.
- L010 VERIFIED: branch workflow filters fixed to NEXY.ai; only NEXY.ai branch currently exists.
- L011 PARTIAL: branch protection remains false.
- L012 VERIFIED: current exact-head required workflows are 0/4 success.
- L013 VERIFIED: runner diagnostic smoke workflow also fails before inspectable steps; exact infra root cause UNKNOWN.
- L014 VERIFIED: deployment remains fail-closed/non-deployable rather than falsely claiming success.
- L015 UNCHANGED_BLOCKER: WebGPU production runtime still stub.
- L016 UNCHANGED_PARTIAL: G14 real compiler/cross-arch/tool execution evidence still not present.
- L017 VERIFIED: historical reproducible inherited-control coverage remains 66/301 = 21.93%, PASS 60/PARTIAL 6; completion NOT_PROVEN.
- L018 FINAL: PARTIAL_IMPROVED / RELEASE_BLOCKED / TSA_PRODUCER_MISSING / CI_INFRA_BLOCKED.
