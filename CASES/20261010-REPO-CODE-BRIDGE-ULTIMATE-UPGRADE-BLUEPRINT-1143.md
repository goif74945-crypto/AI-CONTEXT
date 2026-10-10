# Repo Code Bridge — Ultimate Upgrade Blueprint | 2026-10-10
STATE: REQUIREMENT_PROPOSAL_AND_EVIDENCE_SNAPSHOT; NOT IMPLEMENTED
SOURCE_REPOSITORY: ACTIVE_SITE_GATEWAY_SOURCE_NOT_REVERIFIED_IN_THIS_CHAT
CONTROL_REPO_HEAD_BEFORE_WRITE: 0ef6e32ff39351665bf37e20393692f57556f3fc
SITE: https://repo-code-bridge.nexy-code-me.chatgpt.site
SITE_PROJECT_ID_HISTORICAL: appgprj_6ac56b9353f88191873e731529a5dc6f
CONSTRAINTS: NO MUTATION of goif74945-crypto/NEXY.AI- or any NEXY.AI-named repo; only source-authorized gateway implementation. AI-CONTEXT stores control evidence, not substitute for source.
## Live observations (10 Oct 2026)
- runtime_status: gateway_version=0.1.0, site_runtime_version=cloudflare-workers-vinext, GitHub CONNECTED, D1 AVAILABLE/schema READY, read/write/CI backend READY, public search/fetch READY; 15 allowlisted repositories, read_only_repository_count=0.
- repo_status: NEXY.AI- branch NEXY.ai exact HEAD 58b1200bd61b867e917057d0019eea78ea9f6b2a. Bridge advertised gateway_write_policy=ALLOW and push=true. This DOES NOT grant product mutation in this chat.
- NEXY no-match exhaustive test: candidate=889, inspected=889, searched=887, skipped=2, failed=0, matched=0, unique_blobs=887, GraphQL batch=45, REST fallback=0, coverage_scope=ELIGIBLE_UTF8_TEXT_BLOBS, coverage_complete=true, truncated=false, warnings=[].
- NEXY match-heavy query NEXY max_results=3: matched_files=304, results returned=3, results_truncated=true, warning RESULTS_TRUNCATED; inspected 889, failed 0, coverage_complete=true. Search is NOT a full non-text source audit.
- isolated E2E main HEAD 67a0e4cdbe44d66614fd5a51218592bb18abbf60, workflow .github/workflows/repo-code-bridge-smoke.yml is present.
- ci_status historic run 37888500768: conclusion=failure, one job conclusion=failure, failed_steps=[] and empty failure summary. Independent 2026-10-09 logged evidence says job steps=[] and logs 404 BlobNotFound. Root cause UNKNOWN; not proven test failure.
## Historical evidence to rerun, not current guarantees
- https://github.com/goif74945-crypto/AI-CONTEXT/blob/main/CASES/20261009-REPO-CODE-BRIDGE-ENGINEERING-VERIFICATION-001.md: workflow-file commit through Bridge got GitHub 403, while independent GitHub connector workflow write succeeded. Distinguish workflow scope from plain text scope.
- https://github.com/goif74945-crypto/AI-CONTEXT/blob/main/CASES/20261009-REPO-CODE-BRIDGE-ENGINEERING-VERIFICATION-002.md: normal text commit through Bridge succeeded, same idempotency key replay returned same commit on tested case; E2E CI still pre-step failure.
- https://github.com/goif74945-crypto/AI-CONTEXT/blob/main/CASES/20261009-REPO-CODE-BRIDGE-ENGINEERING-VERIFICATION-003.md: classifier in isolated E2E test passed 16 local Node VM tests, local validator passed 31; production gateway integration NOT verified then.
- https://github.com/goif74945-crypto/AI-CONTEXT/blob/main/CASES/20261009-REPO-CODE-BRIDGE-BATCH-SEARCH-PERFORMANCE-003.md: historical Site source version 15 deployed and measured eligible-text GraphQL batch search, 8.880 s no match on 884 candidates at historical HEAD, 20 tests passed; those values are not universal SLOs.
## Priority requirements for the next AI
P0-01 Verify current writable source and authenticated deployment provenance of exact active Site project; fail closed if not available.
P0-02 Create per-operation capability probe and distinguish config READY vs actual workflow-write, plain-write, runner scheduling, and execution success.
P0-03 Enforce policy deny-by-default for all repository/branch/path/mutation scopes; NEXY.AI- READ ONLY unless a new explicit scoped owner command.
P0-04 Strict SHA compare-and-swap, single-writer leases with fencing token, transactional idempotency, append-only audit, rollback and negative tests.
P0-05 Full CI state machine PRE_DISPATCH / DISPATCHED / QUEUED / PRE_STEP_FAILURE / RUNNING / FAILED_TEST / SUCCEEDED / CANCELLED / BLOCKED and full provider evidence with job-step/log missing classifications.
P0-06 Publish typed schemas for all MCP tools, discriminated success/errors, coverage and provenance; do not conflate result truncation with scan coverage.
P1-01 Repository graph + symbol/AST index incremental by Git blob and tree SHA; scope/aliases/renames, type-aware and language-agnostic fallback.
P1-02 Query planner routing literal/regex/symbol/semantic/graph, exact line and Git blob citations, recall/precision benchmark with adversarial fixtures.
P1-03 Large repo strategy with bounded GraphQL batch and REST fallback, rate-limit-aware adaptive scheduling, conditional persistence and cache.
P1-04 Test runner backed by actual authorized isolated environment; deterministic setup, retry classifier, signed receipts, source/test proof.
P1-05 Change planner, minimal atomic patch, dependency impact graph, semantic diff, compile/test/negative cases, independent verifier before commit.
P1-06 Pipeline security: OAuth/MCP version compatibility, least privilege tokens, SSRF/path injection protections, secret redaction, immutable logs, supply-chain protections.
P1-07 Enterprise-quality dashboard: repo read/write policy, diff/test/CI statuses, evidence, approvals, performance, mobile and WCAG accessibility.
P1-08 Multi-agent orchestrator with bounded task budget, no fake background worker, checkpoint/recovery, one writer and independent auditor.
P2-01 Code-quality and architecture review, dependency scanning, migration safety, risk-aware rollback, SBOM and provenance.
P2-02 Change-aware security and test selection with audit of skipped tests and high-risk mandatory gates.
P2-03 PR Review, selective auto-fix only under explicit scoped permissions, human signoff for risky operations.
P2-04 Offline/replayable benchmark corpus and fault injection for malformed/binary/CRLF/Unicode/symlink/LFS/submodule/large-repo/permission failure.
P2-05 Cross-repository graph, multiple language support, search memory/context budget manager, structured exports, rate-limit and cost governance.
## Acceptance
- Each requirement has ID, source locator, status PROPOSED/VERIFIED_EXISTING/DEFECT/IMPLEMENTED/TESTED/BLOCKED, actual commands, exits, exact HEAD and blob, immutable time/provenance, negative proof and independent check.
- All code/deployment changes ONLY to verified gateway source using owner authority; isolated E2E tests MAY be changed when authorized; NEVER silently write to NEXY.AI-.
- Separate current live observed FACTS from historic records and proposed future capabilities. No 10x/100% promise absent measured evidence.
- Report final PASS per evidence, PARTIAL if any unverified, BLOCKED only for specific dependency while continuing other safe work.
