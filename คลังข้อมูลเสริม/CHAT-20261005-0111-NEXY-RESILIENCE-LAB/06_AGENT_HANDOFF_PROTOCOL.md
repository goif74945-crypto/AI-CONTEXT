# Lossless Agent Handoff Protocol
A handoff packet contains objective, authoritative sources, authorized/protected scope, verified state, completed mutations and evidence, unknowns/conflicts, failed approaches, exact next safe action, rollback data, SHAs/versions, and verification debt.

Never hand off vague statuses such as “basically done” or “should work”.

Store decisions and binding evidence, not hidden chain-of-thought.

Before mutation a resumed agent must answer: what target, what authority, what protection boundary, what current state, what proof of success, and what rollback/stop condition? If any material answer is UNKNOWN, inspect first.
