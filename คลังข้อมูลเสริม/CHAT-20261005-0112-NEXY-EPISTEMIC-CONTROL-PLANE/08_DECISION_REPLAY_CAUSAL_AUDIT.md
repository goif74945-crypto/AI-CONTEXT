# Decision Replay & Causal Audit
Replay packet: decision_id, normalized request hash, law/policy versions, state snapshots, evidence IDs/hashes, tool refs, deterministic config, candidate IDs, judge rule version, verdict, machine-readable rejection reason codes, timestamps, environment metadata.
Do not store hidden chain-of-thought.
Modes: exact, historical, forward, differential.
If a deterministic decision cannot be replayed from durable artifacts, determinism is NOT_VERIFIED.
Status: DESIGN PROPOSAL.