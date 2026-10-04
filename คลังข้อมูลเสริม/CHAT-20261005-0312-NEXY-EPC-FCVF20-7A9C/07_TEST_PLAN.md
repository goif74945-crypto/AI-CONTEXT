# Verification Plan

## E1 static checks

Run Python `compileall` over `src` and `tests`. Parse every production Python AST and require zero binary-float literals. Source-level float rejection is additionally enforced by canonicalization/Q64 constructors and a unit test.

## E2 unit and negative checks

Exercise Q64 boundaries, overflow/division-by-zero, canonical serialization, receipt field completeness, one-time vote rights, DEFER non-consumption, WIP/insufficient CUT rejection, missing evidence, append-only revisions, semantic duplicate witness law, non-destructive CUT, protected-authority attempts and all 20 registry obligations.

## E3 modeled integration checks

Run bounded exhaustive state exploration across status changes, four critical evidence attachments, two KEEP requests, two CUT requests, DEFER and three protected-authority attack events. Evaluate all 20 obligations on every reached child. Repeat exploration and require identical report/digest.

Run constitutional regression differentials against intentionally weakened vote-budget and protected-authority rules, requiring unsafe states/counterexamples to be detected. Run the end-to-end CLI from empty state through pinned evidence -> READY -> KEEP -> 20-system evaluation.

## Persistence verification

Compute SHA-256 manifest over exact locally tested files. Publish those exact UTF-8 bytes to the unique AI-CONTEXT namespace. Read back all published code/test artifacts and compare Git blob SHA-1 identities against locally calculated Git blob identities. Refresh NEXY exact head and prove no NEXY mutation was performed by this task.

## Evidence-class limits

These checks establish E1/E2 and modeled E3 evidence for the standalone verifier. They do not establish NEXY production integration, E4 user-flow, E5 operational, E6 deployment, or E7 physical evidence.
