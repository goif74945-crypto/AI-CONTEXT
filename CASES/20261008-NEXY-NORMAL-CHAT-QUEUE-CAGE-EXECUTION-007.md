# CASE 20261008-NEXY-NORMAL-CHAT-QUEUE-CAGE-EXECUTION-007
TITLE: Queue cancellation race and missing sandbox enforcement follow-up
CATEGORY: CORRECTNESS / SECURITY
STATUS: OPEN_UNTIL_PRODUCT_REGRESSIONS_RUN
EVIDENCE: packages/queue/dispatch.ts id-only post-enqueue state updates, packages/queue/workers.ts claimed/cancelled paths, packages/phase-f/lo3/cage.ts direct-spawn fallback at product HEAD 44bcb851.
CAUSE/RISK: stale producer may resurrect CANCELLED and queued side effect may race DB CAS; bwrap unavailable can bypass namespace isolation while backend returns linux-cgroup-seccomp.
IMPACT: possible correctness/safety failure under concurrent cancellation; security risk where protected untrusted execution can reach unisolated spawn. Neither incident demonstrated in production.
REMEDY: next command requires genuine interleaving test, durable state+Redis+worker fence, and explicit isolation gating/fail-closed semantics where required. No invented TSA or CI passes.
REGRESSION: real Postgres/Redis interleaving, duplicate retry/abort scenarios, isolation negative tests on supported runner.
PROHIBITIONS: no release approval, no test degradation, no force-push, no unstated branch changes.
NEXT: assigned to same normal chat via command 007.
