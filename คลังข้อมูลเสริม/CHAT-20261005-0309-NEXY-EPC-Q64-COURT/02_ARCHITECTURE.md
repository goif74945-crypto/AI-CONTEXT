# EPC Architecture

```text
Lo4 Candidate / Proposal Forge output
        |
        v
Snapshot Binder -----> Spec + NEXY commit + AI-CONTEXT commit
        |
        v
Case Capsule Compiler
        |
        +--> Entitlement Gate (1 KEEP / 1 CUT per CHAT_ID)
        +--> WIP / Unknown Immunity Gate
        +--> Evidence Sufficiency Gate
        +--> Semantic Duplicate Burden Engine
        +--> Canon Supremacy Firewall
        +--> Dependency Closure Gate
        +--> Counterargument Gate
        +--> Q64.64 Composite Scoring
        |
        v
Advisory Verdict
        |
        +--> Append-only tamper-evident ledger
        +--> Evidence revision lineage
        +--> Promotion review packet (never authorization)
        v
NEXY::JUDGE boundary (external, authoritative)
```

## Failure semantics
- Missing/weak evidence -> NON_VOTE `INSUFFICIENT_EVIDENCE`.
- WIP/DEFER candidate submitted to CUT -> NON_VOTE `DEFER`.
- Canon conflict on KEEP -> NON_VOTE `DEFER`.
- Stale snapshot -> hard freeze exception, because voting against a different commit would make the evidence record false.
- Spent KEEP/CUT entitlement -> hard freeze exception.
- Ledger tamper -> hard freeze exception.

## Numeric law
All court scores are Q64.64 raw bigint decimal strings. Floating point is forbidden for score arithmetic. Cost dimensions (`OVERLAP`, `MAINTENANCE_COST`) are inverted before weighting. The default scoring policy is an AI proposal, not Canon.

## Authority law
A positive EPC result means only that a proposal satisfied this advisory court policy for this exact evidence snapshot. It does not mean NEXY approved it.

The bridge terminates at an external `NEXY::JUDGE` review boundary and cannot execute or mutate Core state.
