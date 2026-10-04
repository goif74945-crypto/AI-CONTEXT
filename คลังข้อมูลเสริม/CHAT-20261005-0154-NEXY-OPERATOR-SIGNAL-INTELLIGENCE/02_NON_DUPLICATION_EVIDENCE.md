# Non-Duplication Evidence

Status: scoped evidence, not a proof of semantic uniqueness across every prose sentence in the repository.

## Repository scan
The supplemental tree inspected contained 1,402 paths and 118 top-level project directories at scan time. Path-name searches found no artifacts containing these operator-signal terms:
- `attention`
- `notification`
- `interrupt`
- `fatigue`
- `milestone`
- `signal`
- `acknow`
- `alert`
- `salience`
- `progress`
- `outcome`

Adjacent systems were inspected to avoid semantic duplication:
- Interaction Economics Lab: measures human touches/friction and redundant confirmations; it does not own notification salience, event-stream compression, outcome deltas, or acknowledgement debt.
- Freeze Bridge Lab: compiles semantic recovery intents after freeze; it does not schedule operator attention or maintain signal debt.
- Proof Sensitivity Lab: mutation-tests proof coverage; unrelated to operator signal delivery.
- Shadow Integration Twin / Interleaving Verifier: conformance/concurrency verification, not human attention routing.

## Boundary decision
This project owns only the deterministic transformation from already-produced system events/state into operator-facing signal priority, delivery, compact milestones, outcome deltas, and acknowledgement debt. It does not own task decision authority, confirmation policy, recovery semantics, or canonical NEXY UI.
