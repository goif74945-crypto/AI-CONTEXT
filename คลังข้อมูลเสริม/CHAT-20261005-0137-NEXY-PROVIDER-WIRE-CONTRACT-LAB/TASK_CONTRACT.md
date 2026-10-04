# Task Contract

- objective: create a new, non-duplicative supplemental NEXY engineering lab that can integrate with NEXY without modifying the NEXY.AI repository.
- target repository: `goif74945-crypto/AI-CONTEXT`
- authorized write scope: a new subdirectory under `คลังข้อมูลเสริม/` only.
- protected scope: every repository whose name contains `NEXY.AI`; all existing unrelated AI-CONTEXT paths.
- authority: current user directive > AI-CONTEXT kernel/rules > NEXY project context.
- source facts used: NEXY is a deterministic control hub; external models are workers; hot-swapping is intended; one verified output or freeze/silence is a stable behavioral rule.
- neighboring concepts inspected: capability negotiation; model/provider substitution safety; capability health routing.
- implementation: standalone Python 3.11 reference package using standard library only.
- evidence required: E1 import/compile, E2 unit/negative/fuzz/replay tests, final repository read-back.
- forbidden actions: no writes to NEXY.AI repositories; no claims of official provider API compatibility; no deployment claim; no hidden provider assumptions.
- stop condition: package, tests, design, evidence, and durable continuation record exist in the new AI-CONTEXT subdirectory and repository read-back verifies them.
