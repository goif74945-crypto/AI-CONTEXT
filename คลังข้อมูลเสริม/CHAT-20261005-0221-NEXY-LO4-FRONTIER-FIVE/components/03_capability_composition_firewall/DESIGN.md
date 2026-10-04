# 03 — Capability Composition Firewall (CCF)

**Class:** `Lo4_AI_PROPOSAL_ONLY`

## Purpose
Detect privilege escalation that appears only after combining capabilities. A tool may safely read a secret; another may safely send network traffic; together they may form an exfiltration path even though neither tool is individually forbidden.

## Model
Each capability declares:
- required privilege tokens;
- granted privilege tokens;
- scope.

Policy declares forbidden token conjunctions. A breadth-first state exploration applies only capabilities in allowed scopes. The first forbidden conjunction produces a deterministic minimal-step witness.

## Invariants
- unapproved scope capability is invisible to the composition search;
- initial forbidden state freezes immediately;
- forbidden conjunction cannot be waived by capability ordering;
- exploration is monotonic in privilege tokens for this reference model;
- repeated capability execution is unnecessary because grants are monotonic.

## Complexity
State exploration is potentially exponential in distinct privilege-token sets. The prototype has `max_steps` and deterministic state de-duplication. Production integration should cap token/capability universes and may use symbolic reachability while preserving witness semantics.

## Security value
This addresses an emergent composition threat rather than per-tool permission validation alone.

## Code/Test
- code: `src/nexy_lo4_frontier/ccf.py`
- tests: `tests/test_ccf.py`, permutation determinism tests.
