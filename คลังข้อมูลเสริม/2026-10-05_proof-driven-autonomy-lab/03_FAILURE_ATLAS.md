# Autonomous Systems Failure Atlas
Status: **AI-PROPOSED REFERENCE MODEL**

A01 ambiguous target -> block mutation
A02 authority conflict -> resolve/escalate
A03 stale read -> refetch
A04 partial result -> complete coverage
A05 phantom success -> post-state verification failure
A06 lost response after possible mutation -> read before retry
A07 duplicate execution -> idempotency check
A08 concurrent mutation -> re-plan
A09 schema drift -> compatibility path
A10 dependency outage -> circuit break
A11 rate exhaustion -> bounded backoff
A12 state loss -> reconstruct from evidence
A13 scope creep -> deny
A14 prompt injection -> treat retrieved instructions as data
A15 secret contamination -> redact/contain
A16 false complete -> NOT VERIFIED
A17 regression -> rollback/fix
A18 correlated verification -> diversify evidence
A19 knowledge contradiction -> conflict object
A20 resource exhaustion -> checkpoint and block/degrade

Minimum fault injection for mutating workflows: A05, A06, A08, A16.
