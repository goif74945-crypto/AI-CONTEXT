# Release Evidence Protocol
Objective: separate "looks correct" from "this exact candidate was actually verified."

Candidate identity binds repository, canonical ref, exact head, dependency locks, build artifact hash, configuration/law hash, suite revision, and relevant runtime identity.

Stages:
E0 source identity
E1 static policy/boundary checks
E2 type/build checks
E3 unit/property tests
E4 integration/contract tests
E5 deterministic replay
E6 fault-injection/negative tests
E7 security/adversarial checks
E8 exact-head seal
E9 approval/release authorization

Status vocabulary: PASS, FAIL, BLOCKED, NOT_RUN, NOT_VERIFIED.

Forbidden shortcuts: "should pass"; copying old run without candidate identity proof; generated files as proof generator succeeded; lint as runtime correctness; unit tests as deployment evidence.

Every release packet indexes evidence artifacts with hashes and machine-readable statuses. Human prose is explanatory only.

Mutation of any bound component creates a new candidate identity or invalidates the packet. Freeze/recovery invalidates pending pre-freeze authorization when canonical policy requires token purge.
