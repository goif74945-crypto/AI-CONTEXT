# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence target |
|---|---|---|---|---|
| R1 | Worker hard-gate eligibility | AI proposal constrained by NEXY no-guess/security principles | `_worker_reasons` | E2 tests: capability, clearance, quarantine |
| R2 | Verifier evidence floor | AI proposal preserving NEXY verification law | `_verifier_reasons` | E2 evidence-floor test |
| R3 | Risk-driven independent verifier | AI proposal; CORE still authoritative | `plan`, `_pair_reasons` | E2 high/critical risk tests |
| R4 | Token/cost/latency are hard ceilings | User objective + AI proposal | `_pair_reasons` | E2 budget tests |
| R5 | Budget cannot downgrade verifier | NEXY evidence integrity | `verifier_required` before pair budget checks | E2 budget-exhaustion test |
| R6 | Stable deterministic selection | NEXY deterministic design target | stable sort + lexicographic key | E2 reorder/tie test |
| R7 | Integer price arithmetic | AI proposal aligned with deterministic-core direction | `_price` | E1 inspection + E2 cost selection |
| R8 | Elimination trace | AI proposal for auditability | `Elimination` records | E2 clearance test + read-back |
| R9 | Duplicate identity rejected | AI proposal for state integrity | `_validate_unique_agent_ids` | E2 duplicate-ID test |
| R10 | Planning never claims proof | NEXY verification law | `verification_status=NOT_VERIFIED` | E2 plan assertion |
| R11 | Contract schema is machine-readable | AI-CONTEXT creation law | JSON Schema artifact | E1 JSON parse |
| R12 | NEXY.AI repo protected | Explicit user constraint | execution boundary | E0 mutation audit |

## Evidence boundary
This ledger proves only the reference artifact scope. It does not prove NEXY.AI integration, real provider metadata correctness, production scalability, security hardening, integration behavior, E2E behavior, runtime recovery or deployment.
