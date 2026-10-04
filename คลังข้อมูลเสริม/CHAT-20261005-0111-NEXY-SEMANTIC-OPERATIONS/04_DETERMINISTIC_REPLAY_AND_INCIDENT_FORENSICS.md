# Deterministic Replay and Incident Forensics
## Objective
Make agent failures reconstructable without storing hidden chain-of-thought.
## Replay capsule
run_id; parent_run_id; request_hash; normalized_task_contract; policy_revision; context_snapshot_refs; model/provider identifier; tool schema revisions; tool inputs/outputs; external observation timestamps; mutation receipts; inspectable reason codes; test/eval results; final status; artifact hashes.
Never store secrets or private reasoning.
## Determinism levels
D0 final output only.
D1 traceable inputs/outputs/revisions.
D2 replayable using recorded external fixtures.
D3 reproducible software/config state transitions.
D4 deterministic byte/state equivalence where components permit.
Probabilistic generation is not D4 merely because temperature is low.
## Incident workflow
DETECT -> FREEZE MUTATION -> SNAPSHOT -> CLASSIFY -> REPLAY -> MINIMIZE -> FIX -> REGRESSION -> RELEASE -> POSTMORTEM.
## Mutation receipt
target; before_revision; requested_mutation; after_revision; actor; authorization_ref; timestamp; verification_result; rollback_ref.
## Replay hazards
Live API calls alter evidence; mutable config referenced only by name; timezone/locale missing; tool schemas changed; retry/concurrency ordering omitted; redaction destroys identity relationships.
## Verification
Seed known incidents and prove reconstruction of root-cause-relevant state.
