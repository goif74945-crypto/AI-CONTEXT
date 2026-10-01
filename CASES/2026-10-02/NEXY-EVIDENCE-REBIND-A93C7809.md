TASK_ID: NEXY-CONSOLIDATED-REPAIR-A93C7809-20261002
title: Consolidated remaining repair/build block after sandbox import repair
mode: AUDIT/CROSS
timestamp_source: 2026-10-02T03:29+07:00
target_repo: goif74945-crypto/NEXY.AI-
target_branch: NEXY.ai
target_head: a93c780972ed7464bfc5f182d54129c54d0393cc
target_tree: 07b19ad2e0ffb63ffdc958197d8e7d1bfd9654f9
canonical_design_sha256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
sanitization: no secrets, credentials, private personal data, or provider secret values stored

CASE_ID: CASE-NEXY-EVIDENCE-REBIND-A93C7809
cause: source defect was repaired, producing a new commit while validation identity remains pinned to the previously tested SHA
impact: exact-head pipeline fails before tests despite source tree equality with the previously successful tree
fix: set tested SHA to current HEAD, keep tested tree equal to current tree, mint a new rerun nonce, execute the full gate
status: OPEN
severity: S4 release blocker
